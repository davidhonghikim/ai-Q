const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

// Read package.json
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));

// Function to check if a package version exists
function checkPackageVersion(packageName, version) {
  try {
    const result = execSync(`nodejs-portable\\node-v20.11.0-win-x64\\npm.cmd view ${packageName}@${version} version`, { 
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return { exists: true, version: result.trim() };
  } catch (error) {
    try {
      // Try to get the latest version
      const latestResult = execSync(`nodejs-portable\\node-v20.11.0-win-x64\\npm.cmd view ${packageName} version`, { 
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      });
      return { exists: false, latestVersion: latestResult.trim() };
    } catch (latestError) {
      return { exists: false, error: 'Package not found' };
    }
  }
}

// Function to validate all dependencies
function validateDependencies(dependencies, type) {
  const results = {
    valid: [],
    invalid: [],
    notFound: []
  };

  console.log(`\n=== Validating ${type} ===`);
  
  for (const [packageName, version] of Object.entries(dependencies)) {
    console.log(`Checking ${packageName}@${version}...`);
    
    const check = checkPackageVersion(packageName, version);
    
    if (check.exists) {
      results.valid.push({ package: packageName, version: version });
      console.log(`  ✓ ${packageName}@${version} - VALID`);
    } else if (check.latestVersion) {
      results.invalid.push({ 
        package: packageName, 
        currentVersion: version, 
        latestVersion: check.latestVersion 
      });
      console.log(`  ✗ ${packageName}@${version} - INVALID (latest: ${check.latestVersion})`);
    } else {
      results.notFound.push({ package: packageName, version: version });
      console.log(`  ✗ ${packageName}@${version} - NOT FOUND`);
    }
  }
  
  return results;
}

// Main validation
console.log('Starting comprehensive dependency validation...\n');

const depsResults = validateDependencies(packageJson.dependencies, 'Dependencies');
const devDepsResults = validateDependencies(packageJson.devDependencies, 'Dev Dependencies');

// Summary
console.log('\n=== VALIDATION SUMMARY ===');
console.log(`\nDependencies:`);
console.log(`  Valid: ${depsResults.valid.length}`);
console.log(`  Invalid: ${depsResults.invalid.length}`);
console.log(`  Not Found: ${depsResults.notFound.length}`);

console.log(`\nDev Dependencies:`);
console.log(`  Valid: ${devDepsResults.valid.length}`);
console.log(`  Invalid: ${devDepsResults.invalid.length}`);
console.log(`  Not Found: ${devDepsResults.notFound.length}`);

// Generate corrected package.json
if (depsResults.invalid.length > 0 || depsResults.notFound.length > 0 || 
    devDepsResults.invalid.length > 0 || devDepsResults.notFound.length > 0) {
  
  console.log('\n=== GENERATING CORRECTED PACKAGE.JSON ===');
  
  // Create corrected package.json
  const correctedPackageJson = { ...packageJson };
  
  // Fix dependencies
  depsResults.invalid.forEach(item => {
    correctedPackageJson.dependencies[item.package] = item.latestVersion;
    console.log(`  Fixed ${item.package}: ${item.currentVersion} → ${item.latestVersion}`);
  });
  
  depsResults.notFound.forEach(item => {
    delete correctedPackageJson.dependencies[item.package];
    console.log(`  Removed ${item.package} (not found)`);
  });
  
  // Fix devDependencies
  devDepsResults.invalid.forEach(item => {
    correctedPackageJson.devDependencies[item.package] = item.latestVersion;
    console.log(`  Fixed ${item.package}: ${item.currentVersion} → ${item.latestVersion}`);
  });
  
  devDepsResults.notFound.forEach(item => {
    delete correctedPackageJson.devDependencies[item.package];
    console.log(`  Removed ${item.package} (not found)`);
  });
  
  // Write corrected package.json
  fs.writeFileSync('package.json.corrected', JSON.stringify(correctedPackageJson, null, 2));
  console.log('\nCorrected package.json saved as package.json.corrected');
  
  // Show what needs to be fixed
  console.log('\n=== ISSUES TO FIX ===');
  
  if (depsResults.invalid.length > 0) {
    console.log('\nDependencies with incorrect versions:');
    depsResults.invalid.forEach(item => {
      console.log(`  ${item.package}: ${item.currentVersion} → ${item.latestVersion}`);
    });
  }
  
  if (depsResults.notFound.length > 0) {
    console.log('\nDependencies not found:');
    depsResults.notFound.forEach(item => {
      console.log(`  ${item.package}@${item.version}`);
    });
  }
  
  if (devDepsResults.invalid.length > 0) {
    console.log('\nDev Dependencies with incorrect versions:');
    devDepsResults.invalid.forEach(item => {
      console.log(`  ${item.package}: ${item.currentVersion} → ${item.latestVersion}`);
    });
  }
  
  if (devDepsResults.notFound.length > 0) {
    console.log('\nDev Dependencies not found:');
    devDepsResults.notFound.forEach(item => {
      console.log(`  ${item.package}@${item.version}`);
    });
  }
  
} else {
  console.log('\n✓ All dependencies are valid!');
}

console.log('\nValidation complete.'); 