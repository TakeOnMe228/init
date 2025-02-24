#!/usr/bin/env python3

import json
import os
import sys

def generate_package_json(project_path):
    """
    Generate a minimal package.json file with local dev dependencies,
    and scripts for building and starting a TypeScript project.
    (Uses 'build' folder instead of 'dist'.)
    """
    package_data = {
        "name": os.path.basename(project_path),
        "version": "1.0.0",
        "main": "index.js",
        "scripts": {
            "build": "tsc",
            "start": "node build/index.js",
            "build:start": "npm run build && npm run start"
        },
        "devDependencies": {
            "typescript": "latest"
        },
        "_moduleAliases": {
            "@": "build"
        }
    }

    package_json_path = os.path.join(project_path, "package.json")
    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)


def generate_tsconfig_json(project_path):
    """
    Generate a tsconfig.json that:
    - Targets ES2020
    - Uses NodeNext modules/resolution so .js extensions get auto-appended
    - Outputs compiled JS to the 'build' directory
    - Assumes source files live in 'src'
    - Sets up a path alias '@' to point to 'src'
    """
    true = True
    false = False
    tsconfig_data = {
    "compilerOptions": {
        "target": "ES2020",              
        "module": "commonjs",          
        "outDir": "./build",              
        "rootDir": "./src",              
        "strict": true,                     
        "esModuleInterop": true,            
        "skipLibCheck": true,              
        "forceConsistentCasingInFileNames": true,
        "baseUrl": ".", 
        "paths": {
            "@/*": ["src/*"],
            "!/*": ["./*"]    
        }
    },
    "include": ["src/**/*.ts"],          
    "exclude": ["node_modules"]           
    }


    tsconfig_json_path = os.path.join(project_path, "tsconfig.json")
    with open(tsconfig_json_path, "w") as f:
        json.dump(tsconfig_data, f, indent=2)


def ensure_src_index_ts(project_path):
    """
    Optionally create a 'src' directory with a simple 'index.ts'
    if none exists, just to have a starting point.
    """
    src_path = os.path.join(project_path, "src")
    index_path = os.path.join(src_path, "index.ts")

    if not os.path.exists(src_path):
        os.makedirs(src_path)

    if not os.path.isfile(index_path):
        with open(index_path, "w") as f:
            f.write('import { hello } from "./module";\n\n')
            f.write('hello();\n')

    # Optionally, create another module file to show extension auto-appending
    module_path = os.path.join(src_path, "module.ts")
    if not os.path.isfile(module_path):
        with open(module_path, "w") as f:
            f.write('export function hello() {\n')
            f.write('  console.log("Hello from a separate module!");\n')
            f.write('}\n')


def main():
    # Figure out the project path from command-line arg or default to current dir
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
        if os.path.isabs(project_name):
            project_path = project_name
        else:
            project_path = os.path.join(os.getcwd(), project_name)
    else:
        # If no argument is provided, default to current directory name
        project_path = os.getcwd()

    # Make sure the project folder exists
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    print(f"Initializing TypeScript project in: {project_path}")

    generate_package_json(project_path)
    generate_tsconfig_json(project_path)
    ensure_src_index_ts(project_path)

    print("Success! The following files have been created/updated:")
    print(f"  - {os.path.join(project_path, 'package.json')}")
    print(f"  - {os.path.join(project_path, 'tsconfig.json')}")
    print(f"  - {os.path.join(project_path, 'src/index.ts')}")
    print("\nNext steps:")
    print("  1. cd into your project directory.")
    print("  2. Run `npm install` to install local dev dependencies (TypeScript).")
    print("  3. Run `npm run build` to compile TypeScript => JavaScript in build/.")
    print("  4. Run `npm run start` to execute the compiled JS from build/.")
    print("\nNow your ESM imports in the compiled code will have '.js' appended automatically!")

if __name__ == "__main__":
    main()

