import re
from pathlib import Path
from .graph import build_app


def to_snake_case(name: str) -> str:
    """Convert project name to snake_case for directory names."""
    # Insert underscores before uppercase letters and convert to lowercase
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return name.lower().replace('-', '_').replace(' ', '_')


def get_user_input(prompt: str, default: str = "") -> str:
    """Get input from user with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    return response in ['y', 'yes']


def main():
    print("🚀 FastAPI Boilerplate Generator")
    print("=" * 50)
    print()
    
    # Get project configuration interactively
    project_name = get_user_input("Project name", "my_fastapi_app")
    
    print("\nDatabase options:")
    print("  1. PostgreSQL (recommended for production)")
    print("  2. SQLite (good for development)")
    db_choice = get_user_input("Choose database [1/2]", "1")
    db = "postgres" if db_choice == "1" else "sqlite"
    
    include_docker = get_yes_no("\nInclude Docker support?", True)
    
    print("\nCI/CD options:")
    print("  1. GitHub Actions")
    print("  2. GitLab CI")
    print("  3. None")
    ci_choice = get_user_input("Choose CI/CD [1/2/3]", "1")
    ci_map = {"1": "github", "2": "gitlab", "3": "none"}
    ci = ci_map.get(ci_choice, "github")
    
    # Build natural language request
    db_name = "PostgreSQL" if db == "postgres" else "SQLite"
    ci_name = {"github": "GitHub Actions", "gitlab": "GitLab CI", "none": "no CI/CD"}.get(ci, "GitHub Actions")
    docker_text = "Docker and " if include_docker else ""
    
    user_request = f"Generate a FastAPI backend called '{project_name}' with {db_name}, {docker_text}{ci_name}."
    
    print("\n" + "=" * 50)
    print("📝 Configuration Summary:")
    print(f"  • Project: {project_name}")
    print(f"  • Database: {db_name}")
    print(f"  • Docker: {'Yes' if include_docker else 'No'}")
    print(f"  • CI/CD: {ci_name}")
    print("=" * 50)
    print()
    
    proceed = get_yes_no("Generate project with these settings?", True)
    if not proceed:
        print("❌ Generation cancelled.")
        return
    
    print("\n⏳ Generating project...")
    
    # Generate the project
    app = build_app()
    state = {"user_request": user_request, "config": None, "files": None}
    result = app.invoke(state)

    files = result.get("files") or {}
    
    # Use project name in snake_case for output directory
    project_dir_name = to_snake_case(project_name)
    out_dir = Path(project_dir_name)
    out_dir.mkdir(exist_ok=True)

    for path, content in files.items():
        file_path = out_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    print(f"\n✅ Successfully generated project in: {out_dir.resolve()}")
    print("\n📖 Next steps:")
    print(f"  1. cd {project_dir_name}")
    print("  2. make install")
    print("  3. make run")
    print("\n💡 See README.md for more details!")


if __name__ == "__main__":
    main()
