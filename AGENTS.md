# Project Change Approval Rule

Before changing any project file or creating a new one, prepare a proposed diff and show it in Visual Studio Code for the user to review. This applies to source code, tests, documentation, configuration, generated files, formatting, migrations, and asset changes. Local commands are allowed without separate approval, provided they follow this project-file approval rule. Internet access is allowed without separate approval when no project data is sent externally. Do not send project data to external services without the user’s approval.

## Required workflow

1. Inspect the relevant project state and prepare the exact proposed contents or patch outside the project workspace. Do not edit, create, delete, rename, format, generate, or otherwise modify project files while preparing the proposal. Local commands that do not modify project files may be run without approval.
2. Open a VS Code comparison for every affected file using its current contents and the proposed contents. For a new file, compare an empty file with the proposed file. Summarize the intended change and identify the visible diff.
3. Ask the user to approve the displayed diff. Wait for explicit approval before applying any part of it to the project. A request to implement a feature or fix an issue is not approval of a specific diff.
4. Apply only the approved changes. If the implementation changes after approval, show the revised diff and obtain approval again before applying the revision.
5. If VS Code diff preview is unavailable, leave the project files untouched and tell the user what is needed to show the preview.

Do not treat unrelated or previously approved changes as covered by an approval. Do not create a project file as part of preparing its own approval preview; compare its proposed content against an empty file first.
