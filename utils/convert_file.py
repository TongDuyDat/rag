import pypandoc
import subprocess
def convert_to_pdf(input_file, output_file):
    try:
        subprocess.run(["unoconv", "-f", "pdf", "-o", output_file, input_file], check=True)
        print("Chuyển đổi thành công:", output_file)
        return True
    except subprocess.CalledProcessError as e:
        print("Lỗi khi chuyển đổi:", e)
        return False
