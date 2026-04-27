Explore and map the codebase for: $ARGUMENTS

Steps:
1. Run `find . -type f | grep -v node_modules | grep -v .git | head -60` to get file tree
2. Identify the main entry points
3. Read the top-level README or CLAUDE.md if present
4. Trace the relevant code path for the given topic
5. Produce a summary with:
   - **Architecture**: how the pieces fit together
   - **Key files**: path + one-line description for each important file
   - **Data flow**: how data moves through the system
   - **Where to look**: specific files/functions relevant to $ARGUMENTS

Keep the summary under 300 words. No code unless it's critical for understanding.
