# Agent Guidelines for SetMiddle.io

This file contains instructions, commands, and rules for AI assistants (such as Claude Code and Gemini) working on this repository.

## Commands

- **Compile Firmware**: `esphome compile config.yaml`
- **Upload/Run Firmware**: `esphome run config.yaml`
- **Run Graphify Full Rebuild**: `powershell -File run_graphify.ps1`
- **Update Graphify (Incremental)**: `powershell -File run_graphify_update.ps1`
- **Serve Documentation Wiki**: `powershell -File serve_wiki.ps1`

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost). On Windows/high-core machines, prefix it with `$env:GRAPHIFY_MAX_WORKERS=32;` (PowerShell) or `set GRAPHIFY_MAX_WORKERS=32 &&` (CMD) to avoid the `max_workers must be <= 61` error.

## Automatic Commit After Verification

Whenever you make code changes or add new files to the repository:
1. Ensure all implementation steps and the verification plan are completed successfully.
2. Automatically stage and commit the changes (including any new files) with a concise, descriptive commit message. Do not wait for the user to explicitly ask you to commit them.

## NotebookLM MCP CLI (`nlm`)

**IMPORTANT: You have access to the global NotebookLM MCP CLI via the command `nlm`.** This command provides a unified CLI for Google NotebookLM.

### Key Guidelines for using `nlm`

1. **Non-interactive execution**: Always use the `--confirm` flag for all generation/delete commands to avoid interactive blocking prompts. Do NOT start interactive chats or REPL (e.g., do not run `nlm chat start` or `nlm notebook chat start`). Use `nlm notebook query` or `nlm query notebook` instead for one-shot Q&A.
2. **Authentication**: Always run `nlm login` first if any auth error occurs or credentials are not configured.
3. **Download workflow**: Audio/video takes 1-5 minutes to generate. Poll status with `nlm studio status <notebook-id>` or `nlm status artifacts <notebook-id>`, get the artifact ID, and then download using `nlm download <type> <notebook-id> <artifact-id>`.
4. **Safety & Aliases**: Use `nlm alias` to set aliases for convenience. Always ask the user before performing any deletions (`nlm delete`).
