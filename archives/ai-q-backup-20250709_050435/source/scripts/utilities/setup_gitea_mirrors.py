#!/usr/bin/env python3
"""
Gitea Mirror Setup and Archive Script
Sets up automatic mirroring from GitHub to Gitea for all repositories
and runs the archive script to ensure proper backup.
"""

import json
import requests
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gitea_mirror_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GiteaMirrorSetup:
    def __init__(self, gitea_url="http://localhost:3002", username="thedangerdawg", password="overKill7*nice"):
        self.gitea_url = gitea_url
        self.username = username
        self.password = password
        self.auth_header = {
            'Authorization': f'Basic {self._encode_auth()}',
            'Content-Type': 'application/json'
        }
        
        # Repository mappings: GitHub URL -> Gitea repo name
        self.repositories = {
            "https://github.com/davidhonghikim/ai-Q.git": "ai-Q",
            "https://github.com/davidhonghikim/griot.git": "griot", 
            "https://github.com/davidhonghikim/kai-cd.git": "kai-cd",
            "https://github.com/davidhonghikim/chatdemon.git": "chatdemon"
        }
    
    def _encode_auth(self):
        """Encode username:password for Basic Auth"""
        import base64
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()
    
    def get_repo_id(self, repo_name):
        """Get repository ID from Gitea API"""
        try:
            url = f"{self.gitea_url}/api/v1/repos/{self.username}/{repo_name}"
            response = requests.get(url, headers=self.auth_header)
            if response.status_code == 200:
                return response.json()['id']
            else:
                logger.error(f"Failed to get repo ID for {repo_name}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting repo ID for {repo_name}: {e}")
            return None
    
    def setup_mirror(self, repo_name, github_url):
        """Set up mirror for a repository"""
        repo_id = self.get_repo_id(repo_name)
        if not repo_id:
            logger.error(f"Cannot set up mirror for {repo_name}: repo not found")
            return False
        
        try:
            # Create mirror configuration
            mirror_data = {
                "repo_name": repo_name,
                "repo_id": repo_id,
                "mirror_address": github_url,
                "mirror_interval": "10m",  # Check every 10 minutes
                "enable_prune": True,
                "enable_stats": True,
                "lfs": False,
                "lfs_endpoint": "",
                "lfs_username": "",
                "lfs_password": "",
                "ssh_key_file": "",
                "known_hosts_file": "",
                "tls_cert_file": "",
                "tls_key_file": "",
                "username": "",
                "password": "",
                "private_key": "",
                "passphrase": "",
                "mirror": True,
                "size": 0,
                "wiki": False,
                "milestones": False,
                "labels": False,
                "releases": False,
                "sign_commits": False,
                "archived": False,
                "default_branch": "main"
            }
            
            # Set up mirror via API
            url = f"{self.gitea_url}/api/v1/repos/{self.username}/{repo_name}/mirror"
            response = requests.post(url, headers=self.auth_header, json=mirror_data)
            
            if response.status_code in [200, 201]:
                logger.info(f"Successfully set up mirror for {repo_name}")
                return True
            else:
                logger.error(f"Failed to set up mirror for {repo_name}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting up mirror for {repo_name}: {e}")
            return False
    
    def setup_all_mirrors(self):
        """Set up mirrors for all repositories"""
        logger.info("Starting Gitea mirror setup...")
        
        success_count = 0
        for github_url, repo_name in self.repositories.items():
            logger.info(f"Setting up mirror for {repo_name}...")
            if self.setup_mirror(repo_name, github_url):
                success_count += 1
            time.sleep(1)  # Rate limiting
        
        logger.info(f"Mirror setup completed: {success_count}/{len(self.repositories)} successful")
        return success_count == len(self.repositories)
    
    def run_archive_script(self):
        """Run the archive script to backup the project"""
        logger.info("Running archive script...")
        
        try:
            # Get current timestamp for archive name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"ai-q-backup-{timestamp}"
            
            # Run the archive script
            script_path = Path(__file__).parent / "archive_project.py"
            cmd = [
                sys.executable, str(script_path),
                ".", f"./archives/{archive_name}",
                "--verbose"
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                logger.info("Archive script completed successfully")
                logger.info(f"Archive output: {result.stdout}")
                return True
            else:
                logger.error(f"Archive script failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running archive script: {e}")
            return False
    
    def verify_mirrors(self):
        """Verify that mirrors are working correctly"""
        logger.info("Verifying mirrors...")
        
        for github_url, repo_name in self.repositories.items():
            try:
                url = f"{self.gitea_url}/api/v1/repos/{self.username}/{repo_name}"
                response = requests.get(url, headers=self.auth_header)
                
                if response.status_code == 200:
                    repo_data = response.json()
                    mirror_info = repo_data.get('mirror', {})
                    
                    if mirror_info.get('mirror', False):
                        logger.info(f"✓ {repo_name}: Mirror is active")
                    else:
                        logger.warning(f"⚠ {repo_name}: Mirror not active")
                else:
                    logger.error(f"✗ {repo_name}: Cannot verify mirror status")
                    
            except Exception as e:
                logger.error(f"✗ {repo_name}: Error verifying mirror: {e}")
    
    def run_full_setup(self):
        """Run complete setup: mirrors + archive"""
        logger.info("=== Starting Complete Gitea Mirror and Archive Setup ===")
        
        # Step 1: Set up mirrors
        logger.info("Step 1: Setting up Gitea mirrors...")
        mirror_success = self.setup_all_mirrors()
        
        # Step 2: Verify mirrors
        logger.info("Step 2: Verifying mirrors...")
        self.verify_mirrors()
        
        # Step 3: Run archive script
        logger.info("Step 3: Running archive script...")
        archive_success = self.run_archive_script()
        
        # Summary
        logger.info("=== Setup Summary ===")
        logger.info(f"Mirror setup: {'✓ SUCCESS' if mirror_success else '✗ FAILED'}")
        logger.info(f"Archive script: {'✓ SUCCESS' if archive_success else '✗ FAILED'}")
        
        if mirror_success and archive_success:
            logger.info("🎉 Complete setup successful!")
            return True
        else:
            logger.error("❌ Setup completed with errors")
            return False

def main():
    """Main function"""
    try:
        # Create setup instance
        setup = GiteaMirrorSetup()
        
        # Run full setup
        success = setup.run_full_setup()
        
        if success:
            print("\n✅ Setup completed successfully!")
            print("📋 Next steps:")
            print("1. Check Gitea web UI at http://localhost:3002")
            print("2. Verify mirrors are active in repository settings")
            print("3. Test by pushing to GitHub and checking Gitea sync")
            print("4. Check archive in ./archives/ directory")
        else:
            print("\n❌ Setup completed with errors. Check logs for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 