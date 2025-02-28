# image_editor.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform

class ImageEditorDialog(QDialog):
    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plume Editor - Éditeur d'image")
        self.resize(800, 600)
        self.image_path = image_path
        self.original_pixmap = None
        self.current_pixmap_item = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.graphicsView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        layout.addWidget(self.graphicsView)

        # Contrôles de rotation et d'échelle
        control_layout = QHBoxLayout()

        self.rotateSlider = QSlider(Qt.Horizontal)
        self.rotateSlider.setRange(-180, 180)
        self.rotateSlider.setValue(0)
        self.rotateSlider.valueChanged.connect(self.updateImage)
        control_layout.addWidget(QLabel("Rotation:"))
        control_layout.addWidget(self.rotateSlider)

        self.scaleSlider = QSlider(Qt.Horizontal)
        self.scaleSlider.setRange(10, 300)  # échelle en pourcentage
        self.scaleSlider.setValue(100)
        self.scaleSlider.valueChanged.connect(self.updateImage)
        control_layout.addWidget(QLabel("Échelle (%):"))
        control_layout.addWidget(self.scaleSlider)

        layout.addLayout(control_layout)

        # Boutons pour charger une image, accepter ou annuler
        btn_layout = QHBoxLayout()
        loadBtn = QPushButton("Charger une image")
        loadBtn.clicked.connect(self.loadImage)
        btn_layout.addWidget(loadBtn)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        btn_layout.addWidget(buttonBox)
        layout.addLayout(btn_layout)

        if self.image_path:
            self.loadImage(self.image_path)

    def loadImage(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Charger une image", "", "Images (*.png *.jpg *.bmp *.gif)")
            if not path:
                return
        self.image_path = path
        self.original_pixmap = QPixmap(path)
        self.displayImage()

    def displayImage(self):
        self.scene.clear()
        self.current_pixmap_item = QGraphicsPixmapItem(self.original_pixmap)
        self.scene.addItem(self.current_pixmap_item)
        self.graphicsView.fitInView(self.current_pixmap_item, Qt.KeepAspectRatio)

    def updateImage(self):
        if not self.original_pixmap:
            return
        angle = self.rotateSlider.value()
        scale_percent = self.scaleSlider.value() / 100.0
        transform = QTransform()
        transform.rotate(angle)
        transform.scale(scale_percent, scale_percent)
        transformed = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
        self.scene.clear()
        self.current_pixmap_item = QGraphicsPixmapItem(transformed)
        self.scene.addItem(self.current_pixmap_item)
        self.graphicsView.fitInView(self.current_pixmap_item, Qt.KeepAspectRatio)

    def getEditedPixmap(self):
        if self.current_pixmap_item:
            return self.current_pixmap_item.pixmap()
        return None
