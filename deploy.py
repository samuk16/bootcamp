import os
import subprocess
import logging
import shutil
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("deploy.log"),  # Guarda logs en un archivo
        logging.StreamHandler()  # También muestra logs en consola
    ]
)
logger = logging.getLogger(__name__)

def run_command(command: list[str], error_message: str) -> bool:
    """Ejecuta un comando y maneja errores."""
    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_message}: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error(f"Comando no encontrado: {command[0]}")
        return False

def deploy(
    repo_dir: str = "./", 
    branch: str = "main", 
    source_file: str = "index.html", 
    dest_dir: str = "destino"
) -> bool:
    """Automatiza el proceso de despliegue."""
    try:
        # Cambiar al directorio del repositorio
        os.chdir(repo_dir)
        logger.info(f"Trabajando en el directorio: {repo_dir}")

        # Actualizar el repositorio
        logger.info("Obteniendo el código del repositorio Git...")
        if not run_command(["git", "pull", "origin", branch], "Error al ejecutar git pull"):
            return False

        # Ejecutar pruebas (si existen)
        logger.info("Ejecutando pruebas (si las hay)...")
        # Ejemplo: unittest discover
        # if not run_command(["python", "-m", "unittest", "discover"], "Error en las pruebas"):
        #     return False

        # Crear el paquete o copiar archivos
        logger.info("Creando el directorio de destino...")
        dest_path = Path(dest_dir)
        dest_path.mkdir(exist_ok=True)

        # Copiar archivo usando shutil para mayor portabilidad
        source_path = Path(source_file)
        if not source_path.exists():
            logger.error(f"El archivo {source_file} no existe")
            return False

        logger.info(f"Desplegando {source_file} a {dest_dir}...")
        shutil.copy(source_path, dest_path / source_path.name)

        logger.info(f"Despliegue completado en {dest_dir}")
        return True

    except Exception as e:
        logger.error(f"Error inesperado durante el despliegue: {str(e)}")
        return False

if __name__ == "__main__":
    # Configuración personalizable
    config = {
        "repo_dir": ".",  # Directorio del repositorio
        "branch": "main",  # Rama de Git
        "source_file": "index.html",  # Archivo a desplegar
        "dest_dir": "destino"  # Directorio destino
    }

    success = deploy(**config)
    if not success:
        logger.error("El despliegue falló")
        exit(1)
    else:
        logger.info("El despliegue fue exitoso")
