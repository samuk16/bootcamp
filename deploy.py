import os
import subprocess

def deploy(repo_dir=".", branch="main", source_file="index.html", dest_dir="destino"):
    """Automatiza el despliegue de un archivo."""
    print(f"Cambiando al directorio: {repo_dir}")
    os.chdir(repo_dir)

    print("Actualizando el repositorio Git...")
    subprocess.run(["git", "pull", "origin", branch])

    print(f"Creando el directorio {dest_dir}...")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print(f"Copiando {source_file} a {dest_dir}...")
    if os.path.exists(source_file):
        subprocess.run(["cp", source_file, dest_dir])
        print(f"Despliegue completado en {dest_dir}")
    else:
        print(f"Error: El archivo {source_file} no existe")
        return False

    return True

if __name__ == "__main__":
    # Configuración
    config = {
        "repo_dir": ".",        # Directorio del repositorio
        "branch": "main",       # Rama de Git
        "source_file": "index.html",  # Archivo a copiar
        "dest_dir": "destino"   # Carpeta de destino
    }

    if deploy(**config):
        print("Despliegue exitoso")
    else:
        print("El despliegue falló")
