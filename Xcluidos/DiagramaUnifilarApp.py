import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets, QtCore, QtUiTools
import os

class DiagramaUnifilarApp(QtWidgets.QWidget):
    def __init__(self):
        super(DiagramaUnifilarApp, self).__init__()

        # Ruta al archivo .ui
        ui_file_path = "C:\\Users\\mmfallas\\OneDrive - Caja Costarricense de Seguro Social\\Documentos\\FreeCAD\\Macros\\diagrama_unifilar_ejemplo.ui"

        if not os.path.exists(ui_file_path):
            FreeCAD.Console.PrintError("El archivo UI no se encontró en la ruta especificada.\n")
            return

        # Cargar la UI usando QUiLoader
        try:
            loader = QtUiTools.QUiLoader()
            ui_file = QtCore.QFile(ui_file_path)
            if not ui_file.open(QtCore.QFile.ReadOnly):
                FreeCAD.Console.PrintError("No se pudo abrir el archivo UI.\n")
                return
            
            # Cargar el diseño en el widget actual
            self.ui = loader.load(ui_file, self)
            ui_file.close()

            # Configurar la ventana principal
            self.setWindowTitle("Diagrama Unifilar")
            self.resize(800, 600)

            # Conectar los botones o widgets
            self.setup_connections()
        
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error al cargar la interfaz: {str(e)}\n")
            return

    def setup_connections(self):
        """
        Configura las conexiones entre los elementos de la UI y las funciones de la clase.
        """
        try:
            # Conexión para el botón "pushButton"
            if hasattr(self.ui, "pushButton"):
                self.ui.pushButton.clicked.connect(self.on_pushButton_clicked)

            # Conexión para el botón "btnAgregarComponente"
            if hasattr(self.ui, "btnAgregarComponente"):
                self.ui.btnAgregarComponente.clicked.connect(self.on_btnAgregarComponente_clicked)

            # Conexión para el botón "btnDibujarConexion"
            if hasattr(self.ui, "btnDibujarConexion"):
                self.ui.btnDibujarConexion.clicked.connect(self.on_btnDibujarConexion_clicked)

        except Exception as e:
            FreeCAD.Console.PrintError(f"Error al configurar conexiones: {str(e)}\n")

    # Métodos para cada botón
    def on_pushButton_clicked(self):
        """
        Acción para el botón genérico 'pushButton'.
        """
        FreeCAD.Console.PrintMessage("¡Botón 'PushButton' clickeado!\n")

    def on_btnAgregarComponente_clicked(self):
        """
        Acción para el botón 'Agregar Componente'.
        """
        FreeCAD.Console.PrintMessage("¡Botón 'Agregar Componente' clickeado!\n")

    def on_btnDibujarConexion_clicked(self):
        """
        Acción para el botón 'Dibujar Conexión'.
        """
        FreeCAD.Console.PrintMessage("¡Botón 'Dibujar Conexión' clickeado!\n")

# Comprobar si la aplicación se ejecuta dentro de FreeCAD
if FreeCADGui:
    try:
        app = DiagramaUnifilarApp()
        app.show()
    except Exception as e:
        FreeCAD.Console.PrintError(f"Error al inicializar la aplicación: {str(e)}\n")
