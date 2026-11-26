# Test Grade Calculator – DSP301x Assignment 2

Chương trình chấm điểm bài thi trắc nghiệm 25 câu cho từng lớp. Chương trình làm bốn việc:

1. Đọc file đáp án của một lớp.
2. Kiểm tra từng dòng dữ liệu và báo các dòng không hợp lệ kèm lý do.
3. Chấm điểm, rồi in thống kê của lớp.
4. Lưu điểm từng học sinh ra file `<tên lớp>_grades.txt`.

- Học viên: Vũ Việt Dũng – dungvvFX58282
- Mã nguồn trên GitHub: https://github.com/dungvvFX58282/DSP301x_asm2
- Ngôn ngữ: Python. Các task 1–4 được xử lý bằng **pandas** và **numpy** (task 5).

## Cấu trúc thư mục

```
DSP301x_asm2_dungvvFX58282@funix.edu.vn/
├── vu_dung_grade_the_exams.py   # chương trình chính
├── README.md                    # hướng dẫn này
├── class1.txt … class8.txt      # dữ liệu đầu vào của đề bài
└── class1_grades.txt …          # kết quả, chương trình tạo ra khi chạy
    class8_grades.txt
```

Chương trình tìm file dữ liệu trong **chính thư mục chứa file `.py`**. Vì vậy chương trình vẫn chạy đúng khi được mở từ thư mục khác, ví dụ khi chạy trong IDE.

## Yêu cầu cài đặt

- Python 3.9 trở lên (đã thử với Python 3.14).
- pandas 1.5 trở lên và numpy.

```bash
pip install pandas numpy
```

## Cách chạy

### Từ Command Prompt hoặc Terminal

```bash
cd "đường/dẫn/tới/DSP301x_asm2_dungvvFX58282@funix.edu.vn"
python vu_dung_grade_the_exams.py
```

Trên Windows có thể dùng `py` thay cho `python`.

### Từ Visual Studio Code

1. Mở thư mục bài làm bằng **File → Open Folder**.
2. Mở file `vu_dung_grade_the_exams.py`.
3. Chọn Python interpreter ở góc dưới bên phải.
4. Bấm **Run Python File** (nút ▷ ở góc trên bên phải).
5. Nhập tên lớp trong cửa sổ Terminal.

### Nhập tên lớp

Chương trình hỏi tên lớp cần chấm. Gõ `class1`; gõ `class1.txt` cũng được. Nếu file không tồn tại, chương trình báo `File cannot be found.` và hỏi lại. Mỗi lần chạy chấm một lớp; muốn chấm lớp khác thì chạy lại chương trình.

## Ví dụ một lần chạy

```
Enter a class to grade (i.e. class1 for class1.txt): foobar
File cannot be found.
Enter a class to grade (i.e. class1 for class1.txt): class2
Successfully opened class2.txt

**** ANALYZING ****

Invalid line of data: does not contain exactly 26 values:
N00000023,,A,D,D,C,B,D,A,C,C,,C,,B,A,C,B,D,A,C,A,A

Invalid line of data: N# is invalid
N0000002,B,A,D,D,C,B,D,A,C,D,D,D,A,,A,C,D,,A,C,A,A,B,D,D

Invalid line of data: N# is invalid
NA0000027,B,A,D,D,,B,,A,C,B,D,B,A,,A,C,B,D,A,,A,A,B,D,D

Invalid line of data: does not contain exactly 26 values:
N00000035,B,A,D,D,B,B,,A,C,,D,B,A,B,A,A,B,D,A,C,A,C,B,D,D,A,A


**** REPORT ****

Total valid lines of data: 21
Total invalid lines of data: 4

Total student of high scores: 7
Mean (average) score: 78.00
Highest score: 100
Lowest score: 66
Range of scores: 34
Median score: 76
Question that most people skip: 22 - 6 - 0.286
Question that most people answer incorrectly: 18 - 5 - 0.238

Saved grades to class2_grades.txt
```

File `class2_grades.txt` chứa mỗi dòng một học sinh hợp lệ, theo dạng `ID,điểm`, ví dụ `N00000021,68`.

## Cách chương trình hoạt động

| Task | Hàm | Cách làm |
|---|---|---|
| 1. Mở file | `open_class_file()` | Đọc file bằng `pd.read_csv` trong khối `try/except FileNotFoundError`. Mỗi dòng được đọc nguyên vẹn thành một chuỗi, nên các dòng hỏng vẫn đọc được. Không dùng chuỗi `if` so sánh tên file. |
| 2. Kiểm tra dữ liệu | `analyze_lines()` | Tách mỗi dòng bằng `str.split(",")`. Dòng hợp lệ phải có đúng **26 giá trị**, và giá trị đầu tiên phải là `N` + **8 chữ số** (regex `N\d{8}`). Chương trình kiểm tra số giá trị trước, rồi mới kiểm tra mã học sinh. |
| 3. Chấm điểm | `grade()`, `report_statistics()` | numpy so sánh cả ma trận bài làm (n × 25) với đáp án cùng lúc. Đúng được **+4**, bỏ trống được **0**, sai bị **−1**. |
| 4. Ghi kết quả | `save_grades()` | `DataFrame.to_csv` ghi file `<tên lớp>_grades.txt` cạnh file dữ liệu. |

Các thống kê ở task 3:

- Số học sinh đạt điểm cao (> 80).
- Điểm trung bình.
- Điểm cao nhất, điểm thấp nhất.
- Miền giá trị (cao nhất − thấp nhất).
- Trung vị: nếu số học sinh chẵn thì lấy trung bình hai giá trị giữa.
- Câu bị bỏ qua nhiều nhất và câu bị trả lời sai nhiều nhất, theo dạng `số câu - số học sinh - tỉ lệ`. Nếu nhiều câu có cùng số lượng thì liệt kê đủ tất cả. Tỉ lệ tính trên số bài hợp lệ và làm tròn 3 chữ số thập phân, theo lưu ý của đề.

## Kiểm tra với đầu ra mẫu

Đã chạy chương trình cho cả 8 lớp và so sánh với thư mục `Expected Output` của đề:

- **File điểm:** cả 8 file `classN_grades.txt` trùng khớp từng byte với file mẫu.
- **Báo cáo:** các dòng dữ liệu không hợp lệ kèm lý do, số dòng hợp lệ và không hợp lệ, điểm trung bình, cao nhất, thấp nhất, miền giá trị và trung vị đều khớp `part3_expectedoutput.txt`.

| Lớp | Dòng hợp lệ | Dòng lỗi | Trung bình | Cao nhất | Thấp nhất | Trung vị |
|---|---:|---:|---:|---:|---:|---:|
| class1 | 20 | 0 | 75.60 | 91 | 59 | 73 |
| class2 | 21 | 4 | 78.00 | 100 | 66 | 76 |
| class3 | 100 | 0 | 76.24 | 96 | 56 | 77 |
| class4 | 491 | 4 | 75.76 | 100 | 44 | 77 |
| class5 | 1000 | 0 | 75.60 | 100 | 40 | 77 |
| class6 | 300 | 1 | 75.90 | 100 | 49 | 77 |
| class7 | 193 | 7 | 74.85 | 100 | 47 | 75 |
| class8 | 49 | 0 | 76.67 | 92 | 59 | 77 |
