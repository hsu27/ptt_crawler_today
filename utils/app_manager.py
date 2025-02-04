import os
import logging


class AppManager:
    def __init__(
        self,
        drive="",
        sub_dir_path="",
        app_name="crawptt_project",
    ):
        """
        初始化應用程式資料夾
        drive: 指定存放磁碟 (預設 D)
        sub_dir: 中間目錄 (例如 "Apps")
        app_name: 應用程式名稱
        """
        self.app_dir = os.path.join(f"{drive}:/", sub_dir_path, app_name).replace(
            "\\", "/"
        )

        self.data_dir = os.path.join(self.app_dir, "data").replace(
            "\\", "/"
        )  # 存放 txt 檔案
        self.log_dir = os.path.join(self.app_dir, "logs").replace(
            "\\", "/"
        )  # 存放 log 檔案
        self.log_file = os.path.join(self.log_dir, "app.log").replace("\\", "/")

        # 確保資料夾存在
        self.create_directories()
        self.setup_logging()

        self.write_log("應用程式啟動！")

        # print(f"📁 資料夾設定完成，儲存位置：{self.app_dir}")

    def print_info(self):
        print(f"self.app_dir:{self.app_dir}")
        print(f"self.data_dir:{self.data_dir}")
        print(f"self.log_dir:{self.log_dir}")

    def create_directories(self):
        """建立 data 和 logs 資料夾"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def read_last_line(self, filename):
        """讀取 TXT 檔案內容"""
        filepath = os.path.join(self.data_dir, f"{filename}.txt").replace("\\", "/")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()  # 讀取所有行
                last_line = lines[-1] if lines else ""  # 取最後一行
                return last_line

        return f"⚠️ 檔案 {filepath} 不存在！"

    def setup_logging(self):
        """設定 logging"""
        logging.basicConfig(
            level=logging.INFO,
            filename=self.log_file,
            filemode="a",
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            encoding="utf-8",
        )

    def write_log(self, message):
        """寫入 log 訊息"""
        logging.info(message)


# # 測試執行
# if __name__ == "__main__":
#     app = AppManager()

#     print(app.read_txt("BaseballXXXX"))
