import os
import json
import sys
from pathlib import Path

def analyze_project(project_path):
    root = Path(project_path)
    if not root.is_dir():
        print(json.dumps({"error": f"Directory not found: {project_path}"}))
        sys.exit(1)

    package_json_path = root / 'package.json'
    if not package_json_path.exists():
        print(json.dumps({"error": "package.json not found. Not a valid Node/React project."}))
        sys.exit(1)

    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            pkg = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Error parsing package.json: {str(e)}"}))
        sys.exit(1)

    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    
    # Analyze framework
    framework = "React"
    if "next" in deps: framework = "Next.js"
    elif "expo" in deps: framework = "Expo/React Native"

    # Analyze state management
    state_managers = [lib for lib in ["redux", "@reduxjs/toolkit", "zustand", "jotai", "recoil", "mobx"] if lib in deps]
    
    # Analyze data fetching
    data_fetching = [lib for lib in ["@tanstack/react-query", "swr", "apollo-client", "graphql"] if lib in deps]

    # Analyze folder structure
    src_dir = root / 'src'
    base_dir = src_dir if src_dir.exists() else root
    
    folders = [d.name for d in base_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    has_features = 'features' in folders
    has_components = 'components' in folders
    has_hooks = 'hooks' in folders
    has_utils = 'utils' in folders or 'lib' in folders
    
    level = "Beginner"
    if has_features and len(folders) > 5:
        level = "Senior" if "domain" in folders or "core" in folders else "Mid-Level"
    elif has_hooks and has_utils:
        level = "Junior"

    # Recommendations
    recommendations = []
    
    if len(state_managers) > 1:
        recommendations.append("Múltiplos gerenciadores de estado globais detectados. Considere consolidar em apenas um (ex: Zustand) para reduzir complexidade.")
    
    if not data_fetching and framework == "React":
        recommendations.append("Nenhuma biblioteca de data fetching dedicada (como TanStack Query ou SWR) encontrada. Se houver chamadas de API frequentes, adotá-las reduzirá o boilerplate do useEffect.")
    
    if level in ["Beginner", "Junior"] and has_features:
        recommendations.append("A pasta 'features' foi detectada, mas a arquitetura parece inicial. Certifique-se de que o uso de features (Screaming Architecture) é realmente necessário para a complexidade atual.")
        
    if level == "Senior" and not has_features:
        recommendations.append("Projeto parece complexo mas não utiliza modularização por 'features' ou 'domain'. Considere agrupar código por contexto de negócio em vez de tipo técnico.")

    result = {
        "project": pkg.get("name", "Unknown"),
        "framework": framework,
        "inferredLevel": level,
        "stateManagement": state_managers if state_managers else ["Nenhum (ou Context API/Local State)"],
        "dataFetching": data_fetching if data_fetching else ["Fetch/Axios nativo"],
        "detectedFolders": folders,
        "recommendations": recommendations if recommendations else ["A arquitetura parece equilibrada para as ferramentas atuais."]
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze-architecture.py <path_to_project>")
        sys.exit(1)
    analyze_project(sys.argv[1])
