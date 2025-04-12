from langchain.agents import Tool
from tools.mailer import send_email

tool = Tool.from_function(
    func=send_email,
    name="send_email",
    description="..."
)

tool.run({"subject": "Direct call", "body": "This is from tool.run()"})
