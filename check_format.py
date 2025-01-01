from docx import Document

def check_report_format(file_path):
    document = Document(file_path)
    issues = []

    # Quy chuẩn định dạng
    formatting_config = {
        "font": "Times New Roman",
        "font_size": 12,
        "alignment": 3,  # Căn đều
        "line_spacing": 1.5,
        "space_after": 0,
        "space_before": 0,
        "page_margins": {"top": 2.5, "bottom": 2.5, "left": 2.5, "right": 2.0},
        "title_font_size": 14,
        "title_format": "CHƯƠNG",
        "normal_style": "Normal",
        "toc_font": "Times New Roman",
        "toc_font_size": 12,
        "toc_alignment": 3
    }

    # Kiểm tra lề trang
    section = document.sections[0]
    margins = {
        "top": section.top_margin.cm,
        "bottom": section.bottom_margin.cm,
        "left": section.left_margin.cm,
        "right": section.right_margin.cm,
    }
    for margin, value in formatting_config["page_margins"].items():
        if round(margins[margin], 1) != value:
            issues.append({
                "issue": f"Lỗi lề {margin}: {margins[margin]:.1f}cm",
                "recommend": f"Chỉnh lề {margin} thành {value}cm"
            })

    # Kiểm tra từng đoạn văn
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        # Bỏ qua đoạn trắng
        if not text:
            continue
        if text.upper() == "MỤC LỤC":
                    print('mucluc')
                    continue
        # Kiểm tra font chữ, kích thước font, màu sắc, căn lề, khoảng cách dòng, v.v.
        for run in paragraph.runs:
            if run.font.name != formatting_config["font"]:
                issues.append({
                    "issue": f"Lỗi font chữ ở đoạn: '{text}'",
                    "recommend": f"Sử dụng font '{formatting_config['font']}'"
                })
            if run.font.size and run.font.size.pt != formatting_config["font_size"]:
                issues.append({
                    "issue": f"Lỗi kích thước font ở đoạn: '{text}'",
                    "recommend": f"Sử dụng kích thước font {formatting_config['font_size']}pt"
                })
            if run.font.color.rgb is not None and run.font.color.rgb != "000000":
                issues.append({
                    "issue": f"Lỗi màu sắc font ở đoạn: '{text}'",
                    "recommend": "Sử dụng màu đen cho font."
                })

        # Kiểm tra căn lề, khoảng cách dòng, và khoảng cách trước và sau đoạn
        if paragraph.alignment != formatting_config["alignment"]:
            alignment_name = {
                0: "Căn trái", 1: "Căn giữa", 2: "Căn phải", 3: "Căn đều"
            }.get(paragraph.alignment, "Không xác định")
            issues.append({
                "issue": f"Lỗi căn lề ở đoạn: '{text}'",
                "recommend": f"Căn đều đoạn (Hiện tại: {alignment_name})"
            })

       # Kiểm tra nếu khoảng cách dòng không đúng
        if paragraph.paragraph_format.line_spacing != formatting_config["line_spacing"]:
            current_line_spacing = paragraph.paragraph_format.line_spacing  # Lấy khoảng cách dòng hiện tại
            issues.append({
                "issue": f"Lỗi khoảng cách dòng ở đoạn: '{text}'. Khoảng cách dòng hiện tại là {current_line_spacing}.",
                "recommend": f"Sử dụng khoảng cách dòng {formatting_config['line_spacing']}"
            })


        space_after = paragraph.paragraph_format.space_after.pt if paragraph.paragraph_format.space_after else 0
        space_before = paragraph.paragraph_format.space_before.pt if paragraph.paragraph_format.space_before else 0
        if space_after != formatting_config["space_after"]:
            issues.append({
                "issue": f"Lỗi khoảng cách sau đoạn ở đoạn: '{text}'",
                "recommend": f"Sử dụng khoảng cách sau đoạn {formatting_config['space_after']}pt"
            })
        if space_before != formatting_config["space_before"]:
            issues.append({
                "issue": f"Lỗi khoảng cách trước đoạn ở đoạn: '{text}'",
                "recommend": f"Sử dụng khoảng cách trước đoạn {formatting_config['space_before']}pt"
            })

        # Kiểm tra tiêu đề chương
        if formatting_config["title_format"] in text.upper() and paragraph.style.name != "Heading 1":
            issues.append({
                "issue": f"Lỗi định dạng tiêu đề chương ở: '{text}'",
                "recommend": "Sử dụng 'Heading 1' cho tiêu đề chương"
            })

        # Kiểm tra kiểu đoạn văn
        if paragraph.style.name != formatting_config["normal_style"] and not text.upper().startswith(formatting_config["title_format"]):
            issues.append({
                "issue": f"Lỗi kiểu đoạn văn ở đoạn: '{text}'",
                "recommend": f"Sử dụng kiểu đoạn văn '{formatting_config['normal_style']}'"
            })

    # Kiểm tra mục lục
    # issues.extend(check_table_of_contents(document, formatting_config))

    return issues
