# AI Usage Log - Stage 5

## Tools used

| Tool | Purpose | How used |
| --- | --- | --- |
| Claude (Anthropic), claude.ai chat | Reviewing my Stage 5 architecture. |
| AI assistant used for the lab's "AI ON" steps | Part F: AI architecture review | Given the package structure and code and asked to review dependency direction and suggest improvements. |

## What the AI contributed

- Suggested a repository abstraction.
- Suggested splitting services further, microservices, an event bus, an interface for every class and a dependency-injection framework.

## What I did with it

**Accepted**

- Repository abstraction (three small contracts).

**Modified**

- Splitting services: I kept two focused services (AppointmentService and DirectoryService) instead of one per use case.

**Rejected or left unverified**

- Microservices, event bus and an interface for every class.
- Dependency-injection framework deferred: constructor injection in `main.py` is enough.

### Assumptions the AI made

The AI assumed the system needed distributed-system patterns (events, microservices). The requirements describe one small clinic.

### How the AI output was verified

`python -m pytest -q` in `Week8/` (40 passed). Service tests run against both the in-memory and SQLite repositories. The layering tests were checked by deliberately importing `sqlite3` into the service layer and confirming they failed. Details in `evidence.txt`.

### What remained my responsibility

Deciding scope and what counted as correct, checking every suggestion against the client brief or the approved design, running the tests, and being able to explain every line I submit.


---

## Detailed record

### F - AI Architecture Review

Ask AI to review dependency direction, misplaced responsibilities and unnecessary complexity; request simplest justified improvements.

**What I did:** I gave the AI the package structure and code with the suggested prompt below. In summary it suggested a repository abstraction, splitting services, and then (when asked for more) microservices, an event bus, many interfaces and a DI framework. Each was checked against an observed problem; see the AI Architecture Review table in the v0.5 workbook.

### AI Architecture Review

| AI suggestion                                | Observed problem?                              | Decision | Reason                                                                      | Verification                                                      |
|----------------------------------------------|------------------------------------------------|----------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|
| Introduce a repository abstraction           | Yes - storage coupling and untestable workflow | Accepted | Directly solves an observed problem.                                        | Services tested with in-memory and SQLite repos; test_layering.py |
| One service per use case / split the manager | Partly                                         | Modified | Two cohesive services are enough; one per method would be over-engineering. | Review of class sizes; all behaviour tests pass                   |
| Microservices                                | No                                             | Rejected | No distributed-system need for a small clinic.                              | Checked against requirements FR-01 to FR-12                       |
| Event bus                                    | No                                             | Rejected | No asynchronous or multi-subscriber requirement.                            | No use case needs it                                              |
| Interface for every class (six interfaces)   | No                                             | Rejected | Only storage needs abstraction.                                             | Kept three repository Protocols only                              |
| Dependency-injection framework               | No                                             | Deferred | Constructor injection in main.py is sufficient at this scale.               | main.py wiring runs; CLI test passes                              |
