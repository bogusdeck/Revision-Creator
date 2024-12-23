from flask import Flask, render_template, request
import markdown

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        bug_title = request.form['bug_title']
        error_message = request.form.get('error_message')
        sentry_link = request.form.get('sentry_link')
        issue_description = request.form['issue_description']
        fix_description = request.form['fix_description']
        before_after_table_needed = 'before_after_table_needed' in request.form
        preview_table_needed = 'preview_table_needed' in request.form
        markdown_content = generate_markdown(
            task_id,
            bug_title,
            error_message,
            sentry_link,
            issue_description,
            fix_description,
            before_after_table_needed,
            preview_table_needed
        )

        html_content = markdown.markdown(markdown_content)

        return render_template('result.html', markdown_content=markdown_content, html_content=html_content,
                               task_id=task_id, bug_title=bug_title, error_message=error_message,
                               sentry_link=sentry_link, issue_description=issue_description,
                               fix_description=fix_description, before_after_table_needed=before_after_table_needed,
                               preview_table_needed=preview_table_needed)

    return render_template('result.html', markdown_content='', html_content='',
                           task_id='', bug_title='', error_message='', sentry_link='',
                           issue_description='', fix_description='', before_after_table_needed=False,
                           preview_table_needed=False)

def generate_markdown(task_id, bug_title, error_message, sentry_link, issue_description, fix_description, before_after_table_needed, preview_table_needed):
    markdown_content = ""

    if task_id:
        markdown_content += f"FIXES {task_id}\n\n"
    
    markdown_content += f"**{bug_title}**\n\n"

    if error_message:
        markdown_content += f"BUG:\n> \n> {error_message.replace('\n', '\n> ')}\n\n"

    if sentry_link:
        markdown_content += f"Sentry error: [[ {sentry_link} ]]\n\n"

    if issue_description:
        markdown_content += f"**ISSUE:**\n{issue_description}\n\n"
    
    if fix_description:
        markdown_content += f"**FIX:**\n{fix_description}\n\n"

    if before_after_table_needed:
        markdown_content += f"| Before | After |\n|--------|-------|\n| {before_after_table_needed} | {before_after_table_needed} |\n"

    if preview_table_needed:
        markdown_content += f"\n| Preview |  |\n|---------|-----|\n| {preview_table_needed} | {preview_table_needed} |\n"

    return markdown_content

