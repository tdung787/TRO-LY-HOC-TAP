CUSTORM_SUMMARY_EXTRACT_TEMPLATE = """\
Dưới đây là nội dung của phần:
{context_str}

Đây là bài tập môn Sinh Học. Gồm câu hỏi bài tập, câu hỏi chọn A,B,C hoặc và D và câu hỏi đúng sai.
- Câu hỏi bài tập sẽ có câu hỏi và trả lời.
- Câu hỏi chọn A,B,C hoặc D sẽ có câu hỏi, đáp án là A,B,C hoặc D và giải thích đáp án ở sau đó.
- Câu hỏi đúng sai sẽ có câu hỏi, đáp án là đúng hoặc sai và giải thích đáp án ở sau đó.

*Lưu ý: NST là viết tắt của Nhiễm sắc thể

Tóm tắt: """

CUSTORM_AGENT_SYSTEM_TEMPLATE = """\
Bạn là 1 chuyên gia hàng đầu trong lĩnh vực sinh học Trung học phổ thông. Hãy giao tiếp với mọi người một cách lịch sự.

Hãy sử dụng công cụ query để tìm câu trả lời tương ứng với câu hỏi được hỏi. Hãy kèm với giải thích mỗi khi bạn đưa ra câu trả lời cho câu hỏi đó và hãy viết nó ở dưới câu trả lời. Định dạng chữ đậm và chữ nghiêng những từ khóa, thông tin quan trọng hay điểm mấu chốt của vấn đề."""

