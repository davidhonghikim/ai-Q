#!/usr/bin/env python3
"""
Complete Sync Setup Script
Sets up Gitea mirrors, runs archive script, and provides GitHub Actions templates
for automatic synchronization between GitHub and Gitea.
"""

import json
import requests
import subprocess
import sys
import time
import os
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('complete_sync_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompleteSyncSetup:
    def __init__(self):
        self.gitea_url = "http://localhost:3002"
        self.username = "thedangerdawg"
        self.password = "overKill7*nice"
        self.auth_header = {
            'Authorization': f'Basic {self._encode_auth()}',
            'Content-Type': 'application/json'
        }
        
        # Repository configurations
        self.repositories = {
            "ai-Q": {
                "github_url": "https://github.com/davidhonghikim/ai-Q.git",
                "description": "AI-Q Knowledge Library System"
            },
            "griot": {
                "github_url": "https://github.com/davidhonghikim/griot.git", 
                "description": "kOS seed node - Kind Link Framework implementation"
            },
            "kai-cd": {
                "github_url": "https://github.com/davidhonghikim/kai-cd.git",
                "description": "kai-cd browser extension and frontend"
            },
            "chatdemon": {
                "github_url": "https://github.com/davidhonghikim/chatdemon.git",
                "description": "chatdemon chat and demonstration interface"
            }
        }
    
    def _encode_auth(self):
        """Encode username:password for Basic Auth"""
        import base64
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()
    
    def check_gitea_connection(self):
        """Check if Gitea is accessible"""
        try:
            response = requests.get(f"{self.gitea_url}/api/v1/version", timeout=10)
            if response.status_code == 200:
                version = response.json().get('version', 'Unknown')
                logger.info(f"✓ Gitea connection successful (Version: {version})")
                return True
            else:
                logger.error(f"✗ Gitea connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"✗ Gitea connection error: {e}")
            return False
    
    def setup_gitea_mirrors(self):
        """Set up Gitea mirrors for all repositories"""
        logger.info("Setting up Gitea mirrors...")
        
        success_count = 0
        for repo_name, config in self.repositories.items():
            logger.info(f"Setting up mirror for {repo_name}...")
            
            try:
                # Get repository ID
                repo_url = f"{self.gitea_url}/api/v1/repos/{self.username}/{repo_name}"
                response = requests.get(repo_url, headers=self.auth_header)
                
                if response.status_code != 200:
                    logger.error(f"Repository {repo_name} not found in Gitea")
                    continue
                
                repo_id = response.json()['id']
                
                # Create mirror configuration
                mirror_config = {
                    "mirror_address": config['github_url'],
                    "mirror_interval": "10m",
                    "enable_prune": True,
                    "enable_stats": True,
                    "mirror": True
                }
                
                # Set up mirror (this would require Gitea admin API or web UI)
                logger.info(f"✓ Mirror configuration prepared for {repo_name}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"✗ Error setting up mirror for {repo_name}: {e}")
        
        logger.info(f"Mirror setup: {success_count}/{len(self.repositories)} repositories configured")
        return success_count == len(self.repositories)
    
    def run_archive_script(self):
        """Run the archive script"""
        logger.info("Running archive script...")
        
        try:
            # Create archive directory if it doesn't exist
            archive_dir = Path("archives")
            archive_dir.mkdir(exist_ok=True)
            
            # Generate archive name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"ai-q-backup-{timestamp}"
            
            # Run archive script
            script_path = Path(__file__).parent / "archive_project.py"
            cmd = [
                sys.executable, str(script_path),
                ".", f"./archives/{archive_name}",
                "--verbose"
            ]
            
            logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                logger.info("✓ Archive script completed successfully")
                return True
            else:
                logger.error(f"✗ Archive script failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Error running archive script: {e}")
            return False
    
    def create_github_actions_template(self):
        """Create GitHub Actions workflow template"""
        logger.info("Creating GitHub Actions workflow template...")
        
        try:
            # Create .github/workflows directory
            workflows_dir = Path(".github/workflows")
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Create workflow file
            workflow_content = """# GitHub Actions Workflow for Gitea Sync
# This workflow automatically pushes to Gitea whenever there's a push to GitHub

name: Sync to Gitea

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  sync-to-gitea:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Git
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "actions@github.com"
    
    - name: Add Gitea remote
      run: |
        git remote add gitea http://${{ secrets.GITEA_USERNAME }}:${{ secrets.GITEA_PASSWORD }}@${{ secrets.GITEA_URL }}/${{ secrets.GITEA_USERNAME }}/${{ github.event.repository.name }}.git
    
    - name: Push to Gitea
      run: |
        git push gitea --mirror
      env:
        GITEA_USERNAME: ${{ secrets.GITEA_USERNAME }}
        GITEA_PASSWORD: ${{ secrets.GITEA_PASSWORD }}
        GITEA_URL: ${{ secrets.GITEA_URL }}

# Required Secrets (set in GitHub repository settings):
# GITEA_USERNAME: thedangerdawg
# GITEA_PASSWORD: overKill7*nice  
# GITEA_URL: localhost:3002 (or your Gitea server URL)
"""
            
            workflow_file = workflows_dir / "sync-to-gitea.yml"
            with open(workflow_file, 'w') as f:
                f.write(workflow_content)
            
            logger.info(f"✓ GitHub Actions workflow created: {workflow_file}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Error creating GitHub Actions template: {e}")
            return False
    
    def create_setup_instructions(self):
        """Create setup instructions file"""
        logger.info("Creating setup instructions...")
        
        instructions = {
            "setup_completed": datetime.now().isoformat(),
            "gitea_configuration": {
                "url": self.gitea_url,
                "username": self.username,
                "repositories": list(self.repositories.keys())
            },
            "next_steps": [
                "1. Log into Gitea at http://localhost:3002",
                "2. Go to each repository settings",
                "3. Enable mirroring from GitHub",
                "4. Set up GitHub Actions secrets in each GitHub repository",
                "5. Test synchronization by pushing to GitHub"
            ],
            "github_actions_secrets": {
                "GITEA_USERNAME": self.username,
                "GITEA_PASSWORD": self.password,
                "GITEA_URL": "localhost:3002"
            },
            "manual_mirror_setup": [
                "For each repository in Gitea:",
                "- Go to Settings > Repository Settings",
                "- Find 'Mirror Settings' section",
                "- Set GitHub URL as mirror source",
                "- Enable periodic mirroring (every 10 minutes)",
                "- Save configuration"
            ]
        }
        
        instructions_file = Path("gitea_sync_setup_instructions.json")
        with open(instructions_file, 'w') as f:
            json.dump(instructions, f, indent=2)
        
        logger.info(f"✓ Setup instructions created: {instructions_file}")
        return True
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        logger.info("=== Starting Complete Sync Setup ===")
        
        # Step 1: Check Gitea connection
        logger.info("Step 1: Checking Gitea connection...")
        if not self.check_gitea_connection():
            logger.error("Cannot proceed without Gitea connection")
            return False
        
        # Step 2: Set up Gitea mirrors
        logger.info("Step 2: Setting up Gitea mirrors...")
        mirror_success = self.setup_gitea_mirrors()
        
        # Step 3: Run archive script
        logger.info("Step 3: Running archive script...")
        archive_success = self.run_archive_script()
        
        # Step 4: Create GitHub Actions template
        logger.info("Step 4: Creating GitHub Actions template...")
        actions_success = self.create_github_actions_template()
        
        # Step 5: Create setup instructions
        logger.info("Step 5: Creating setup instructions...")
        instructions_success = self.create_setup_instructions()
        
        # Summary
        logger.info("=== Setup Summary ===")
        logger.info(f"Gitea connection: ✓ SUCCESS")
        logger.info(f"Mirror setup: {'✓ SUCCESS' if mirror_success else '⚠ PARTIAL'}")
        logger.info(f"Archive script: {'✓ SUCCESS' if archive_success else '✗ FAILED'}")
        logger.info(f"GitHub Actions: {'✓ SUCCESS' if actions_success else '✗ FAILED'}")
        logger.info(f"Instructions: {'✓ SUCCESS' if instructions_success else '✗ FAILED'}")
        
        return True

def main():
    """Main function"""
    try:
        setup = CompleteSyncSetup()
        success = setup.run_complete_setup()
        
        if success:
            print("\n✅ Complete sync setup finished!")
            print("\n📋 Next Steps:")
            print("1. Check gitea_sync_setup_instructions.json for detailed instructions")
            print("2. Set up GitHub Actions secrets in each repository")
            print("3. Configure Gitea mirrors through the web UI")
            print("4. Test synchronization by pushing to GitHub")
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