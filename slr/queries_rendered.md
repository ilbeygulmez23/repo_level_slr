# Rendered search strings

Window: 2022-01-01 to 2026-09-30. Generated from queries.json; do not edit by hand.

## F1_repo_level_codegen

### arXiv

```
(ti:"repository-level" OR abs:"repository-level" OR ti:"repo-level" OR abs:"repo-level" OR ti:"repository-scale" OR abs:"repository-scale" OR ti:"project-level" OR abs:"project-level" OR ti:"codebase-level" OR abs:"codebase-level" OR ti:"repository-aware" OR abs:"repository-aware" OR ti:"repository context" OR abs:"repository context" OR ti:"cross-file" OR abs:"cross-file" OR ti:"non-standalone" OR abs:"non-standalone" OR ti:"project-specific" OR abs:"project-specific" OR ti:"real-world repositories" OR abs:"real-world repositories" OR ti:"real-world code repositories" OR abs:"real-world code repositories" OR ti:"real-world projects" OR abs:"real-world projects") AND (ti:"code generation" OR abs:"code generation" OR ti:"generating code" OR abs:"generating code" OR ti:"generate code" OR abs:"generate code" OR ti:"code synthesis" OR abs:"code synthesis" OR ti:"program synthesis" OR abs:"program synthesis" OR ti:"code completion" OR abs:"code completion") AND (ti:"language model" OR abs:"language model" OR ti:"language models" OR abs:"language models" OR ti:"LLM" OR abs:"LLM" OR ti:"LLMs" OR abs:"LLMs" OR ti:"agent" OR abs:"agent" OR ti:"agents" OR abs:"agents" OR ti:"agentic" OR abs:"agentic" OR ti:"GPT" OR abs:"GPT" OR ti:"Codex" OR abs:"Codex" OR ti:"foundation model" OR abs:"foundation model" OR ti:"foundation models" OR abs:"foundation models")
```

### OpenAlex

```
("repository-level" OR "repo-level" OR "repository-scale" OR "project-level" OR "codebase-level" OR "repository-aware" OR "repository context" OR "cross-file" OR "non-standalone" OR "project-specific" OR "real-world repositories" OR "real-world code repositories" OR "real-world projects") AND ("code generation" OR "generating code" OR "generate code" OR "code synthesis" OR "program synthesis" OR "code completion") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")
```

### Scopus

```
TITLE-ABS-KEY(("repository-level" OR "repo-level" OR "repository-scale" OR "project-level" OR "codebase-level" OR "repository-aware" OR "repository context" OR "cross-file" OR "non-standalone" OR "project-specific" OR "real-world repositories" OR "real-world code repositories" OR "real-world projects") AND ("code generation" OR "generating code" OR "generate code" OR "code synthesis" OR "program synthesis" OR "code completion") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")) AND PUBYEAR > 2021 AND PUBYEAR < 2027
```

### IEEE Xplore

```
("All Metadata":"repository-level" OR "All Metadata":"repo-level" OR "All Metadata":"repository-scale" OR "All Metadata":"project-level" OR "All Metadata":"codebase-level" OR "All Metadata":"repository-aware" OR "All Metadata":"repository context" OR "All Metadata":"cross-file" OR "All Metadata":"non-standalone" OR "All Metadata":"project-specific" OR "All Metadata":"real-world repositories" OR "All Metadata":"real-world code repositories" OR "All Metadata":"real-world projects") AND ("All Metadata":"code generation" OR "All Metadata":"generating code" OR "All Metadata":"generate code" OR "All Metadata":"code synthesis" OR "All Metadata":"program synthesis" OR "All Metadata":"code completion") AND ("All Metadata":"language model" OR "All Metadata":"language models" OR "All Metadata":"LLM" OR "All Metadata":"LLMs" OR "All Metadata":"agent" OR "All Metadata":"agents" OR "All Metadata":"agentic" OR "All Metadata":"GPT" OR "All Metadata":"Codex" OR "All Metadata":"foundation model" OR "All Metadata":"foundation models")
```

### ACM DL

```
(Title:("repository-level" OR "repo-level" OR "repository-scale" OR "project-level" OR "codebase-level" OR "repository-aware" OR "repository context" OR "cross-file" OR "non-standalone" OR "project-specific" OR "real-world repositories" OR "real-world code repositories" OR "real-world projects") OR Abstract:("repository-level" OR "repo-level" OR "repository-scale" OR "project-level" OR "codebase-level" OR "repository-aware" OR "repository context" OR "cross-file" OR "non-standalone" OR "project-specific" OR "real-world repositories" OR "real-world code repositories" OR "real-world projects")) AND (Title:("code generation" OR "generating code" OR "generate code" OR "code synthesis" OR "program synthesis" OR "code completion") OR Abstract:("code generation" OR "generating code" OR "generate code" OR "code synthesis" OR "program synthesis" OR "code completion")) AND (Title:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models") OR Abstract:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models"))
```

## F2_whole_repo_construction

### arXiv

```
(ti:"repository generation" OR abs:"repository generation" OR ti:"codebase generation" OR abs:"codebase generation" OR ti:"code repository generation" OR abs:"code repository generation" OR ti:"project generation" OR abs:"project generation" OR ti:"software generation" OR abs:"software generation" OR ti:"application generation" OR abs:"application generation" OR ti:"library generation" OR abs:"library generation" OR ti:"NL2Repo" OR abs:"NL2Repo" OR ti:"natural language to code repository" OR abs:"natural language to code repository" OR ti:"entire repository" OR abs:"entire repository" OR ti:"entire repositories" OR abs:"entire repositories" OR ti:"entire codebase" OR abs:"entire codebase" OR ti:"whole repository" OR abs:"whole repository" OR ti:"whole-repository" OR abs:"whole-repository" OR ti:"repository from scratch" OR abs:"repository from scratch" OR ti:"repository reconstruction" OR abs:"repository reconstruction" OR ti:"repository reproduction" OR abs:"repository reproduction" OR ti:"repository translation" OR abs:"repository translation" OR ti:"repository modernization" OR abs:"repository modernization" OR ti:"end-to-end software development" OR abs:"end-to-end software development" OR ti:"end-to-end software generation" OR abs:"end-to-end software generation" OR ti:"end-to-end project development" OR abs:"end-to-end project development" OR ti:"software from scratch" OR abs:"software from scratch") AND (ti:"language model" OR abs:"language model" OR ti:"language models" OR abs:"language models" OR ti:"LLM" OR abs:"LLM" OR ti:"LLMs" OR abs:"LLMs" OR ti:"agent" OR abs:"agent" OR ti:"agents" OR abs:"agents" OR ti:"agentic" OR abs:"agentic" OR ti:"GPT" OR abs:"GPT" OR ti:"Codex" OR abs:"Codex" OR ti:"foundation model" OR abs:"foundation model" OR ti:"foundation models" OR abs:"foundation models")
```

### OpenAlex

```
("repository generation" OR "codebase generation" OR "code repository generation" OR "project generation" OR "software generation" OR "application generation" OR "library generation" OR "NL2Repo" OR "natural language to code repository" OR "entire repository" OR "entire repositories" OR "entire codebase" OR "whole repository" OR "whole-repository" OR "repository from scratch" OR "repository reconstruction" OR "repository reproduction" OR "repository translation" OR "repository modernization" OR "end-to-end software development" OR "end-to-end software generation" OR "end-to-end project development" OR "software from scratch") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")
```

### Scopus

```
TITLE-ABS-KEY(("repository generation" OR "codebase generation" OR "code repository generation" OR "project generation" OR "software generation" OR "application generation" OR "library generation" OR "NL2Repo" OR "natural language to code repository" OR "entire repository" OR "entire repositories" OR "entire codebase" OR "whole repository" OR "whole-repository" OR "repository from scratch" OR "repository reconstruction" OR "repository reproduction" OR "repository translation" OR "repository modernization" OR "end-to-end software development" OR "end-to-end software generation" OR "end-to-end project development" OR "software from scratch") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")) AND PUBYEAR > 2021 AND PUBYEAR < 2027
```

### IEEE Xplore

```
("All Metadata":"repository generation" OR "All Metadata":"codebase generation" OR "All Metadata":"code repository generation" OR "All Metadata":"project generation" OR "All Metadata":"software generation" OR "All Metadata":"application generation" OR "All Metadata":"library generation" OR "All Metadata":"NL2Repo" OR "All Metadata":"natural language to code repository" OR "All Metadata":"entire repository" OR "All Metadata":"entire repositories" OR "All Metadata":"entire codebase" OR "All Metadata":"whole repository" OR "All Metadata":"whole-repository" OR "All Metadata":"repository from scratch" OR "All Metadata":"repository reconstruction" OR "All Metadata":"repository reproduction" OR "All Metadata":"repository translation" OR "All Metadata":"repository modernization" OR "All Metadata":"end-to-end software development" OR "All Metadata":"end-to-end software generation" OR "All Metadata":"end-to-end project development" OR "All Metadata":"software from scratch") AND ("All Metadata":"language model" OR "All Metadata":"language models" OR "All Metadata":"LLM" OR "All Metadata":"LLMs" OR "All Metadata":"agent" OR "All Metadata":"agents" OR "All Metadata":"agentic" OR "All Metadata":"GPT" OR "All Metadata":"Codex" OR "All Metadata":"foundation model" OR "All Metadata":"foundation models")
```

### ACM DL

```
(Title:("repository generation" OR "codebase generation" OR "code repository generation" OR "project generation" OR "software generation" OR "application generation" OR "library generation" OR "NL2Repo" OR "natural language to code repository" OR "entire repository" OR "entire repositories" OR "entire codebase" OR "whole repository" OR "whole-repository" OR "repository from scratch" OR "repository reconstruction" OR "repository reproduction" OR "repository translation" OR "repository modernization" OR "end-to-end software development" OR "end-to-end software generation" OR "end-to-end project development" OR "software from scratch") OR Abstract:("repository generation" OR "codebase generation" OR "code repository generation" OR "project generation" OR "software generation" OR "application generation" OR "library generation" OR "NL2Repo" OR "natural language to code repository" OR "entire repository" OR "entire repositories" OR "entire codebase" OR "whole repository" OR "whole-repository" OR "repository from scratch" OR "repository reconstruction" OR "repository reproduction" OR "repository translation" OR "repository modernization" OR "end-to-end software development" OR "end-to-end software generation" OR "end-to-end project development" OR "software from scratch")) AND (Title:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models") OR Abstract:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models"))
```

## F3_from_scratch_software

### arXiv

```
(ti:"from scratch" OR abs:"from scratch") AND (ti:"repository" OR abs:"repository" OR ti:"repositories" OR abs:"repositories" OR ti:"codebase" OR abs:"codebase" OR ti:"codebases" OR abs:"codebases" OR ti:"software project" OR abs:"software project" OR ti:"software projects" OR abs:"software projects" OR ti:"library" OR abs:"library" OR ti:"libraries" OR abs:"libraries" OR ti:"application" OR abs:"application" OR ti:"applications" OR abs:"applications") AND (ti:"code" OR abs:"code" OR ti:"coding" OR abs:"coding" OR ti:"program" OR abs:"program" OR ti:"programs" OR abs:"programs") AND (ti:"language model" OR abs:"language model" OR ti:"language models" OR abs:"language models" OR ti:"LLM" OR abs:"LLM" OR ti:"LLMs" OR abs:"LLMs" OR ti:"agent" OR abs:"agent" OR ti:"agents" OR abs:"agents" OR ti:"agentic" OR abs:"agentic" OR ti:"GPT" OR abs:"GPT" OR ti:"Codex" OR abs:"Codex" OR ti:"foundation model" OR abs:"foundation model" OR ti:"foundation models" OR abs:"foundation models")
```

### OpenAlex

```
("from scratch") AND ("repository" OR "repositories" OR "codebase" OR "codebases" OR "software project" OR "software projects" OR "library" OR "libraries" OR "application" OR "applications") AND ("code" OR "coding" OR "program" OR "programs") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")
```

### Scopus

```
TITLE-ABS-KEY(("from scratch") AND ("repository" OR "repositories" OR "codebase" OR "codebases" OR "software project" OR "software projects" OR "library" OR "libraries" OR "application" OR "applications") AND ("code" OR "coding" OR "program" OR "programs") AND ("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models")) AND PUBYEAR > 2021 AND PUBYEAR < 2027
```

### IEEE Xplore

```
("All Metadata":"from scratch") AND ("All Metadata":"repository" OR "All Metadata":"repositories" OR "All Metadata":"codebase" OR "All Metadata":"codebases" OR "All Metadata":"software project" OR "All Metadata":"software projects" OR "All Metadata":"library" OR "All Metadata":"libraries" OR "All Metadata":"application" OR "All Metadata":"applications") AND ("All Metadata":"code" OR "All Metadata":"coding" OR "All Metadata":"program" OR "All Metadata":"programs") AND ("All Metadata":"language model" OR "All Metadata":"language models" OR "All Metadata":"LLM" OR "All Metadata":"LLMs" OR "All Metadata":"agent" OR "All Metadata":"agents" OR "All Metadata":"agentic" OR "All Metadata":"GPT" OR "All Metadata":"Codex" OR "All Metadata":"foundation model" OR "All Metadata":"foundation models")
```

### ACM DL

```
(Title:("from scratch") OR Abstract:("from scratch")) AND (Title:("repository" OR "repositories" OR "codebase" OR "codebases" OR "software project" OR "software projects" OR "library" OR "libraries" OR "application" OR "applications") OR Abstract:("repository" OR "repositories" OR "codebase" OR "codebases" OR "software project" OR "software projects" OR "library" OR "libraries" OR "application" OR "applications")) AND (Title:("code" OR "coding" OR "program" OR "programs") OR Abstract:("code" OR "coding" OR "program" OR "programs")) AND (Title:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models") OR Abstract:("language model" OR "language models" OR "LLM" OR "LLMs" OR "agent" OR "agents" OR "agentic" OR "GPT" OR "Codex" OR "foundation model" OR "foundation models"))
```
