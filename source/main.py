import sys
import time
import requests
from pathlib import Path

from PySide6.QtCore import QThread, Signal, QProcess, QUrl, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


USECASES = {
    "chat": {
        "emoji": "💬",
        "title": "General Chat",
        "description": "Fragen beantworten, brainstormen, Alltagshilfe.",
    },
    "writing": {
        "emoji": "✍️",
        "title": "Writing",
        "description": "Texte schreiben, redigieren, zusammenfassen.",
    },
    "coding": {
        "emoji": "💻",
        "title": "Coding",
        "description": "Code schreiben, debuggen, Skripte erstellen.",
    },
    "rag": {
        "emoji": "📄",
        "title": "Document Q&A",
        "description": "Dokumente durchsuchen und Fragen beantworten.",
    },
    "vision": {
        "emoji": "🖼️",
        "title": "Vision",
        "description": "Bilder, Screenshots und OCR verstehen.",
    },
}


MODELS = [
    {
        "name": "Qwen3.5 0.8B Q8_0",
        "size_gb": 1.6,
        "llamafile": "Qwen3.5-0.8B-Q8_0.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile",
        "capabilities": {"chat": 2, "writing": 2, "coding": 1, "rag": 1, "vision": 0},
    },
    {
        "name": "Qwen3.5 2B Q8_0",
        "size_gb": 3.2,
        "llamafile": "Qwen3.5-2B-Q8_0.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-2B-Q8_0.llamafile",
        "capabilities": {"chat": 3, "writing": 3, "coding": 2, "rag": 2, "vision": 0},
    },
    {
        "name": "Ministral 3B Instruct 2512 Q4_K_M",
        "size_gb": 3.4,
        "llamafile": "Ministral-3-3B-Instruct-2512-Q4_K_M.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Ministral-3-3B-Instruct-2512-Q4_K_M.llamafile",
        "capabilities": {"chat": 3, "writing": 3, "coding": 2, "rag": 2, "vision": 0},
    },
    {
        "name": "Qwen3.5 4B Q5_K_S",
        "size_gb": 4.1,
        "llamafile": "Qwen3.5-4B-Q5_K_S.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-4B-Q5_K_S.llamafile",
        "capabilities": {"chat": 3, "writing": 3, "coding": 3, "rag": 3, "vision": 0},
    },
    {
        "name": "LLaVA v1.6 Mistral 7B Q4_K_M",
        "size_gb": 5.3,
        "llamafile": "llava-v1.6-mistral-7b-Q4_K_M.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/llava-v1.6-mistral-7b-Q4_K_M.llamafile",
        "capabilities": {"chat": 3, "writing": 2, "coding": 1, "rag": 3, "vision": 5},
    },
    {
        "name": "Apertus 8B Instruct 2509",
        "size_gb": 5.9,
        "llamafile": "Apertus-8B-Instruct-2509.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Apertus-8B-Instruct-2509.llamafile",
        "capabilities": {"chat": 4, "writing": 3, "coding": 3, "rag": 3, "vision": 0},
    },
    {
        "name": "Qwen3.5 9B Q5_K_S",
        "size_gb": 7.4,
        "llamafile": "Qwen3.5-9B-Q5_K_S.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-9B-Q5_K_S.llamafile",
        "capabilities": {"chat": 4, "writing": 4, "coding": 4, "rag": 4, "vision": 0},
    },
    {
        "name": "Ministral 3B Instruct 2512 BF16",
        "size_gb": 7.8,
        "llamafile": "Ministral-3-3B-Instruct-2512-BF16.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Ministral-3-3B-Instruct-2512-BF16.llamafile",
        "capabilities": {"chat": 4, "writing": 4, "coding": 3, "rag": 3, "vision": 0},
    },
    {
        "name": "LLaVA v1.6 Mistral 7B Q8_0",
        "size_gb": 8.4,
        "llamafile": "llava-v1.6-mistral-7b-Q8_0.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/llava-v1.6-mistral-7b-Q8_0.llamafile",
        "capabilities": {"chat": 3, "writing": 3, "coding": 1, "rag": 3, "vision": 5},
    },
    {
        "name": "gpt-oss 20B MXFP4",
        "size_gb": 12.0,
        "llamafile": "gpt-oss-20b-mxfp4.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/gpt-oss-20b-mxfp4.llamafile",
        "capabilities": {"chat": 5, "writing": 5, "coding": 5, "rag": 5, "vision": 0},
    },
    {
        "name": "gpt-oss 20B Q5_K_S",
        "size_gb": 12.0,
        "llamafile": "gpt-oss-20b-Q5_K_S.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/gpt-oss-20b-Q5_K_S.llamafile",
        "capabilities": {"chat": 5, "writing": 5, "coding": 5, "rag": 5, "vision": 0},
    },
    {
        "name": "LFM2 24B A2B Q5_K_M",
        "size_gb": 16.0,
        "llamafile": "LFM2-24B-A2B-Q5_K_M.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/LFM2-24B-A2B-Q5_K_M.llamafile",
        "capabilities": {"chat": 5, "writing": 5, "coding": 4, "rag": 5, "vision": 0},
    },
    {
        "name": "Qwen3.5 27B Q5_K_S",
        "size_gb": 19.0,
        "llamafile": "Qwen3.5-27B-Q5_K_S.llamafile",
        "url": "https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-27B-Q5_K_S.llamafile",
        "capabilities": {"chat": 5, "writing": 5, "coding": 5, "rag": 5, "vision": 0},
    },
]


def stars(value: int) -> str:
    return "★" * max(0, int(value))


def get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


def exe_name_from_llamafile(filename: str) -> str:
    return filename.replace(".llamafile", ".exe")


def recommend_models(selected_usecases):
    recommended = []
    others = []

    for model in MODELS:
        score = sum(model["capabilities"].get(key, 0) for key in selected_usecases)

        if score > 0:
            recommended.append((score, model, "Recommended"))
        else:
            others.append((score, model, "Other available"))

    recommended.sort(key=lambda item: item[0], reverse=True)
    others.sort(key=lambda item: item[1]["size_gb"])

    return recommended + others


class UseCasePage(QWidget):
    def __init__(self, on_recommend):
        super().__init__()

        self.on_recommend = on_recommend
        self.checkboxes = {}

        layout = QVBoxLayout(self)

        title = QLabel("What do you want to use AI for?")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Select one or more use cases. The app will recommend suitable local AI models."
        )
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 12px;")
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(12)
        layout.addLayout(grid)

        for index, (key, data) in enumerate(USECASES.items()):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet("""
                QFrame {
                    border: 1px solid #3a3a3a;
                    border-radius: 10px;
                    padding: 10px;
                    background: #1e1e1e;
                }
                QFrame:hover {
                    background: #2a2a2a;
                }
            """)

            card_layout = QVBoxLayout(card)

            checkbox = QCheckBox(f'{data["emoji"]}  {data["title"]}')
            checkbox.setStyleSheet("font-size: 16px; font-weight: bold;")

            description = QLabel(data["description"])
            description.setWordWrap(True)
            description.setStyleSheet("font-size: 13px; color: #555;")

            card_layout.addWidget(checkbox)
            card_layout.addWidget(description)

            self.checkboxes[key] = checkbox

            row = index // 3
            col = index % 3
            grid.addWidget(card, row, col)

        button = QPushButton("Recommend Models")
        button.clicked.connect(self.handle_recommend)
        button.setStyleSheet("font-size: 15px; padding: 10px; margin-top: 16px;")
        layout.addWidget(button)

        layout.addStretch()

    def handle_recommend(self):
        selected = [
            key for key, checkbox in self.checkboxes.items()
            if checkbox.isChecked()
        ]

        if not selected:
            QMessageBox.warning(
                self,
                "No use case selected",
                "Please select at least one use case.",
            )
            return

        self.on_recommend(selected)


class RecommendationPage(QWidget):
    def __init__(self, on_download, on_back):
        super().__init__()

        self.on_download = on_download
        self.scored_models = []

        layout = QVBoxLayout(self)

        title = QLabel("Recommended Models + Other Available Models")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget(0, 11)
        self.table.setHorizontalHeaderLabels([
            "Select",
            "Category",
            "Score",
            "Chat",
            "Writing",
            "Coding",
            "RAG",
            "Vision",
            "Model",
            "Size",
            "Llamafile",
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(on_back)
        layout.addWidget(self.back_button)

        self.download_button = QPushButton("Download Selected")
        self.download_button.clicked.connect(self.handle_download)
        layout.addWidget(self.download_button)

    def set_models(self, scored_models):
        self.scored_models = scored_models
        self.table.setRowCount(len(scored_models))

        for row, (score, model, category) in enumerate(scored_models):
            checkbox = QCheckBox()
            checkbox.setChecked(row == 0)
            self.table.setCellWidget(row, 0, checkbox)

            capabilities = model["capabilities"]

            self.table.setItem(row, 1, QTableWidgetItem(category))
            self.table.setItem(row, 2, QTableWidgetItem(stars(score)))
            self.table.setItem(row, 3, QTableWidgetItem(stars(capabilities.get("chat", 0))))
            self.table.setItem(row, 4, QTableWidgetItem(stars(capabilities.get("writing", 0))))
            self.table.setItem(row, 5, QTableWidgetItem(stars(capabilities.get("coding", 0))))
            self.table.setItem(row, 6, QTableWidgetItem(stars(capabilities.get("rag", 0))))
            self.table.setItem(row, 7, QTableWidgetItem(stars(capabilities.get("vision", 0))))
            self.table.setItem(row, 8, QTableWidgetItem(model["name"]))
            self.table.setItem(row, 9, QTableWidgetItem(f'{model["size_gb"]} GB'))
            self.table.setItem(row, 10, QTableWidgetItem(model["llamafile"]))

    def selected_models(self):
        selected = []

        for row, (_, model, _) in enumerate(self.scored_models):
            checkbox = self.table.cellWidget(row, 0)

            if checkbox and checkbox.isChecked():
                selected.append(model)

        return selected

    def handle_download(self):
        selected = self.selected_models()

        if not selected:
            QMessageBox.warning(
                self,
                "No model selected",
                "Please select at least one model.",
            )
            return

        total_size = sum(model["size_gb"] for model in selected)
        model_list = "\n".join(f'- {model["name"]}' for model in selected)

        message = (
            f"You selected:\n\n{model_list}\n\n"
            f"Total download size: {total_size:.1f} GB\n\n"
            f"Files will be saved here:\n{get_app_dir()}"
        )

        result = QMessageBox.question(
            self,
            "Confirm Download",
            message,
            QMessageBox.Yes | QMessageBox.No,
        )

        if result == QMessageBox.Yes:
            self.on_download(selected)


class DownloadWorker(QThread):
    progress = Signal(str, int, str, str, str)
    status = Signal(str)
    finished_all = Signal(list)
    failed = Signal(str, str)

    def __init__(self, models, target_dir: Path):
        super().__init__()

        self.models = models
        self.target_dir = target_dir
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def run(self):
        completed = []

        for model in self.models:
            if self.cancelled:
                self.status.emit("Download cancelled.")
                return

            filename = model["llamafile"]
            url = model["url"]

            temp_path = self.target_dir / f"{filename}.download"
            final_llamafile_path = self.target_dir / filename
            final_exe_path = self.target_dir / exe_name_from_llamafile(filename)

            if final_exe_path.exists():
                self.status.emit(f"Already installed: {final_exe_path.name}")
                completed.append(final_exe_path)
                continue

            try:
                self.status.emit(f"Downloading {filename}...")

                with requests.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()

                    total = int(response.headers.get("content-length", 0))
                    downloaded = 0
                    start_time = time.time()

                    with open(temp_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if self.cancelled:
                                file.close()
                                temp_path.unlink(missing_ok=True)
                                self.status.emit("Download cancelled.")
                                return

                            if chunk:
                                file.write(chunk)
                                downloaded += len(chunk)

                                percent = int(downloaded * 100 / total) if total else 0
                                elapsed = max(time.time() - start_time, 0.1)
                                speed = downloaded / elapsed / (1024 * 1024)

                                self.progress.emit(
                                    filename,
                                    percent,
                                    f"{downloaded / (1024 ** 3):.2f} GB",
                                    f"{total / (1024 ** 3):.2f} GB" if total else "Unknown",
                                    f"{speed:.2f} MB/s",
                                )

                if final_llamafile_path.exists():
                    final_llamafile_path.unlink()

                temp_path.rename(final_llamafile_path)

                if final_exe_path.exists():
                    final_exe_path.unlink()

                final_llamafile_path.rename(final_exe_path)

                self.status.emit(f"Installed {final_exe_path.name}")
                completed.append(final_exe_path)

            except Exception as error:
                temp_path.unlink(missing_ok=True)
                self.failed.emit(filename, str(error))
                return

        self.finished_all.emit(completed)


class DownloadPage(QWidget):
    def __init__(self, on_launch, on_back):
        super().__init__()

        self.on_launch = on_launch
        self.downloaded_paths = []
        self.worker = None

        layout = QVBoxLayout(self)

        title = QLabel("Download Models")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.status_label = QLabel("Ready.")
        layout.addWidget(self.status_label)

        self.file_label = QLabel("")
        layout.addWidget(self.file_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.detail_label = QLabel("")
        layout.addWidget(self.detail_label)

        self.cancel_button = QPushButton("Cancel Download")
        self.cancel_button.clicked.connect(self.cancel_download)
        layout.addWidget(self.cancel_button)

        self.launch_button = QPushButton("Launch First Downloaded Model")
        self.launch_button.setEnabled(False)
        self.launch_button.clicked.connect(self.launch_first_model)
        layout.addWidget(self.launch_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(on_back)
        layout.addWidget(self.back_button)

        layout.addStretch()

    def start_download(self, models):
        self.downloaded_paths = []
        self.progress_bar.setValue(0)
        self.launch_button.setEnabled(False)
        self.status_label.setText("Starting download...")

        self.worker = DownloadWorker(models, get_app_dir())
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished_all.connect(self.download_finished)
        self.worker.failed.connect(self.download_failed)
        self.worker.start()

    def update_progress(self, filename, percent, downloaded, total, speed):
        self.file_label.setText(filename)
        self.progress_bar.setValue(percent)
        self.detail_label.setText(f"{downloaded} / {total} — {speed}")

    def download_finished(self, paths):
        self.downloaded_paths = paths
        self.status_label.setText("Download complete.")
        self.launch_button.setEnabled(bool(paths))
        self.progress_bar.setValue(100)

    def download_failed(self, filename, error):
        QMessageBox.critical(
            self,
            "Download failed",
            f"{filename}\n\n{error}",
        )
        self.status_label.setText("Download failed.")

    def cancel_download(self):
        if self.worker:
            self.worker.cancel()

    def launch_first_model(self):
        if self.downloaded_paths:
            self.on_launch(self.downloaded_paths[0])


class ServerWatcher(QWidget):
    server_ready = Signal()

    def __init__(self, url="http://127.0.0.1:8080"):
        super().__init__()

        self.url = url
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_server)

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def check_server(self):
        try:
            response = requests.get(self.url, timeout=1)

            if response.status_code < 500:
                self.stop()
                self.server_ready.emit()

        except Exception:
            pass


class ModelLauncher:
    def __init__(self):
        self.process = None

    def launch(self, exe_path: Path):
        self.process = QProcess()
        self.process.setProgram(str(exe_path))
        self.process.setWorkingDirectory(str(exe_path.parent))
        self.process.start()

    def stop(self):
        if self.process:
            self.process.kill()
            self.process = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Local AI Model Installer")
        self.resize(1400, 700)

        self.launcher = ModelLauncher()

        self.server_watcher = ServerWatcher()
        self.server_watcher.server_ready.connect(self.open_web_ui)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.usecase_page = UseCasePage(self.show_recommendations)

        self.recommendation_page = RecommendationPage(
            on_download=self.start_download,
            on_back=self.show_usecases,
        )

        self.download_page = DownloadPage(
            on_launch=self.launch_model,
            on_back=self.show_recommendations_from_current,
        )

        self.current_scored_models = []

        self.stack.addWidget(self.usecase_page)
        self.stack.addWidget(self.recommendation_page)
        self.stack.addWidget(self.download_page)

    def show_usecases(self):
        self.stack.setCurrentWidget(self.usecase_page)

    def show_recommendations(self, selected_usecases):
        self.current_scored_models = recommend_models(selected_usecases)
        self.recommendation_page.set_models(self.current_scored_models)
        self.stack.setCurrentWidget(self.recommendation_page)

    def show_recommendations_from_current(self):
        self.stack.setCurrentWidget(self.recommendation_page)

    def start_download(self, models):
        self.stack.setCurrentWidget(self.download_page)
        self.download_page.start_download(models)

    def launch_model(self, exe_path: Path):
        self.launcher.launch(exe_path)
        self.server_watcher.start()

        QMessageBox.information(
            self,
            "Launching model",
            "The model is starting. The web UI will open when the server is ready.",
        )

    def open_web_ui(self):
        QDesktopServices.openUrl(QUrl("http://127.0.0.1:8080"))

    def closeEvent(self, event):
        self.launcher.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())