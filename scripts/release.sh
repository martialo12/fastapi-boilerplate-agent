#!/bin/bash
# Release script for FastAPI Boilerplate Generator
# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 0.2.1

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if version argument is provided
if [ -z "$1" ]; then
    print_error "Version argument required!"
    echo "Usage: ./scripts/release.sh <version>"
    echo "Example: ./scripts/release.sh 0.2.1"
    exit 1
fi

VERSION=$1
TAG="v${VERSION}"

print_info "Starting release process for version ${VERSION}"

# Step 1: Check if we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "You are on branch '${CURRENT_BRANCH}', not 'main'"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Release cancelled"
        exit 1
    fi
fi

# Step 2: Check if working directory is clean
if [[ -n $(git status -s) ]]; then
    print_error "Working directory is not clean. Commit or stash changes first."
    git status -s
    exit 1
fi

# Step 3: Pull latest changes
print_info "Pulling latest changes..."
git pull origin main

# Step 4: Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    print_error "Tag ${TAG} already exists!"
    exit 1
fi

# Step 5: Update version in pyproject.toml
print_info "Updating version in pyproject.toml..."
sed -i.bak "s/^version = .*/version = \"${VERSION}\"/" pyproject.toml
rm pyproject.toml.bak

# Step 6: Check CHANGELOG.md
print_info "Checking CHANGELOG.md..."
if ! grep -q "## \[${VERSION}\]" CHANGELOG.md; then
    print_warning "Version ${VERSION} not found in CHANGELOG.md"
    print_info "Please update CHANGELOG.md with release notes"
    read -p "Open CHANGELOG.md in editor? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        ${EDITOR:-nano} CHANGELOG.md
    fi
fi

# Step 7: Run tests
print_info "Running tests..."
if command -v pytest &> /dev/null; then
    pytest tests/ -v || {
        print_error "Tests failed! Fix issues before releasing."
        exit 1
    }
    print_success "Tests passed"
else
    print_warning "pytest not found, skipping tests"
fi

# Step 8: Build package
print_info "Building package..."
rm -rf dist/ build/ *.egg-info
python -m build || {
    print_error "Build failed!"
    exit 1
}
print_success "Package built successfully"

# Step 9: Check package
print_info "Checking package..."
twine check dist/* || {
    print_error "Package check failed!"
    exit 1
}
print_success "Package check passed"

# Step 10: Show summary
echo ""
echo "========================================"
echo "📦 Release Summary"
echo "========================================"
echo "Version: ${VERSION}"
echo "Tag: ${TAG}"
echo "Branch: ${CURRENT_BRANCH}"
echo "Files to commit:"
echo "  - pyproject.toml"
echo "  - CHANGELOG.md (if updated)"
echo ""
echo "Next steps:"
echo "  1. Commit changes"
echo "  2. Create and push tag"
echo "  3. Create GitHub Release"
echo "========================================"
echo ""

# Step 11: Confirm release
read -p "Proceed with release? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Release cancelled"
    print_info "To undo version change: git checkout pyproject.toml"
    exit 0
fi

# Step 12: Commit changes
print_info "Committing changes..."
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to ${VERSION}" || {
    print_warning "Nothing to commit (version already committed?)"
}

# Step 13: Create tag
print_info "Creating tag ${TAG}..."
git tag -a "$TAG" -m "Release version ${VERSION}"
print_success "Tag ${TAG} created"

# Step 14: Push changes
print_info "Pushing changes to origin..."
git push origin main
git push origin "$TAG"
print_success "Changes pushed"

# Step 15: Final instructions
echo ""
print_success "Release ${VERSION} completed!"
echo ""
print_info "Next steps:"
echo "  1. Go to: https://github.com/martialo12/fastapi-boilerplate-agent/releases/new"
echo "  2. Select tag: ${TAG}"
echo "  3. Set title: ${TAG}"
echo "  4. Copy release notes from CHANGELOG.md"
echo "  5. Publish release"
echo ""
print_info "The GitHub Action will automatically:"
echo "  - Build the package"
echo "  - Publish to Test PyPI"
echo "  - Publish to PyPI"
echo ""
print_info "Monitor the workflow at:"
echo "  https://github.com/martialo12/fastapi-boilerplate-agent/actions"
echo ""
print_success "🎉 Release process complete!"
