#!/usr/bin/env python3
"""
Recipe System Validation Test
Tests the recipe system functionality in isolated environment
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class RecipeSystemTester:
    def __init__(self, test_dir):
        self.test_dir = Path(test_dir)
        self.results = {
            "test_timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": []
        }
    def log_test(self, test_name, status, details=None):
        test_result = {
            "test_name": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.results["test_results"].append(test_result)
        if status == "PASS":
            self.results["tests_passed"] += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.results["tests_failed"] += 1
            print(f"❌ {test_name}: FAILED - {details}")
    def test_recipe_index_loading(self):
        try:
            index_path = self.test_dir / "00-RECIPE_INDEX.json"
            if not index_path.exists():
                self.log_test("Recipe Index Loading", "FAIL", "00-RECIPE_INDEX.json not found")
                return False
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            required_fields = ["metadata", "recipe_categories"]
            missing = [f for f in required_fields if f not in index]
            if missing:
                self.log_test("Recipe Index Loading", "FAIL", f"Missing fields: {missing}")
                return False
            self.log_test("Recipe Index Loading", "PASS", {"categories": list(index["recipe_categories"].keys())})
            return True
        except Exception as e:
            self.log_test("Recipe Index Loading", "FAIL", f"Exception: {str(e)}")
            return False
    def test_recipe_category(self, category, expected_count):
        try:
            cat_dir = self.test_dir / category
            if not cat_dir.exists() or not cat_dir.is_dir():
                self.log_test(f"{category.title()} Directory", "FAIL", f"{category} dir missing")
                return False
            files = list(cat_dir.glob("*.json"))
            if len(files) < expected_count:
                self.log_test(f"{category.title()} Files", "FAIL", f"Expected at least {expected_count}, found {len(files)}")
                return False
            self.log_test(f"{category.title()} Files", "PASS", {"count": len(files)})
            return True
        except Exception as e:
            self.log_test(f"{category.title()} Files", "FAIL", f"Exception: {str(e)}")
            return False
    def run_all_tests(self):
        print("🧪 RECIPE SYSTEM VALIDATION TEST")
        print("=" * 50)
        self.test_recipe_index_loading()
        # Check each category from index
        with open(self.test_dir / "00-RECIPE_INDEX.json", 'r', encoding='utf-8') as f:
            index = json.load(f)
        for cat, info in index.get("recipe_categories", {}).items():
            self.test_recipe_category(cat, info.get("count", 0))
        # Save results
        results_path = self.test_dir / "test_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print("=" * 50)
        print(f"📊 TEST SUMMARY: {self.results['tests_passed']}/{self.results['tests_passed'] + self.results['tests_failed']} tests passed")
        if self.results['tests_failed'] == 0:
            print("✅ All tests passed - Recipe system is functional")
        else:
            print(f"❌ {self.results['tests_failed']} tests failed - Recipe system needs attention")
        print(f"📄 Results saved to: {results_path}")
        return self.results['tests_failed'] == 0

def main():
    test_dir = Path(".")
    if not test_dir.exists():
        print("❌ Test directory not found.")
        sys.exit(1)
    tester = RecipeSystemTester(test_dir)
    success = tester.run_all_tests()
    if success:
        print("\n🎉 Recipe system validation completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️ Recipe system validation found issues that need attention.")
        sys.exit(1)

if __name__ == "__main__":
    main() 