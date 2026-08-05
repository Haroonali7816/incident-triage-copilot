# Evaluation Results

Sample size: 40 hand-labeled incidents (random seed 42, see `generate_eval_sample.py`)

## Methodology

Labels were assigned **blind** — the labeler did not see the LLM's predictions while labeling (see `LABELING_GUIDE.md`), to avoid biasing judgment toward agreeing with the model.

## Agreement

- Severity exact-match accuracy: 40.0%
- Severity Cohen's kappa: 0.026
- Category exact-match accuracy: 50.0%
- Category Cohen's kappa: 0.378

## Disagreements

- **#14484** In FastAPI 0.123.7, annotations from code imported in `if TYPE_CHECKING` could break
  - Human: severity=`low`, category=`bug`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#15714** Implement automatic API documentation generation with interactive examples and SDK generation
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`medium`, category=`feature_request`
  - Notes: (none)

- **#11624** How to use single database connection throughout application. 
  - Human: severity=`low`, category=`question`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#12017** 👷🏻 Recently, the CI is failing due to docs building failures
  - Human: severity=`medium`, category=`bug`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)

- **#12313** Required with Ellipsis may not work
  - Human: severity=`low`, category=`other`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)

- **#14221** Changes to _remap_definitions_and_field_mappings failing in v0.119
  - Human: severity=`medium`, category=`other`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)

- **#14498** Performance issue
  - Human: severity=`low`, category=`other`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#14787** Add Arabic (العربية) documentation translation
  - Human: severity=`low`, category=`documentation`
  - LLM: severity=`low`, category=`feature_request`
  - Notes: (none)

- **#9684** FastAPI Executable File Using conda Environment
  - Human: severity=`low`, category=`other`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#15612** OSV advisory MAL-2026-4750 appears to be a false positive for fastapi/fastapi
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#15680** AI安全审计报告：FastAPI代码质量评估
  - Human: severity=`high`, category=`other`
  - LLM: severity=`low`, category=`other`
  - Notes: (none)

- **#14503** Performance issue
  - Human: severity=`low`, category=`other`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#12402** [BUG] In version 0.115.0 of FastAPI, the pydantic model that has declared an alias cannot correctly receive query parameters
  - Human: severity=`medium`, category=`bug`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)

- **#15713** Add automatic request/response caching with smart cache invalidation strategies
  - Human: severity=`high`, category=`feature_request`
  - LLM: severity=`medium`, category=`feature_request`
  - Notes: (none)

- **#5831** Fastapi 
  - Human: severity=`low`, category=`other`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#9764** FastAPI return response code of 422 when sending image files to test.
  - Human: severity=`medium`, category=`bug`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#12382** HTML WEB SAMPLES FOR TOKEN AUTH
  - Human: severity=`low`, category=`other`
  - LLM: severity=`low`, category=`feature_request`
  - Notes: (none)

- **#9355** When to update the https://fastapi.tiangolo.com/zh/？
  - Human: severity=`medium`, category=`question`
  - LLM: severity=`low`, category=`documentation`
  - Notes: (none)

- **#13533** Multiple regressions in the handling of forms & form validation
  - Human: severity=`low`, category=`other`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)

- **#10720** functools.partial() does not work on an async dependable
  - Human: severity=`high`, category=`feature_request`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#13715** SUB APPLICATIONS - MOUNTS IS SHOW INCORRECT INFORMATION
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`low`, category=`question`
  - Notes: (none)

- **#12419** Question about "Required, can be None" parameter
  - Human: severity=`low`, category=`question`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#10787** Old `HTTPValidationError` and `ValidationError` OpenAPI entry
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#10236** Inconsistent add_api_route types
  - Human: severity=`high`, category=`bug`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#14501** Performance issue
  - Human: severity=`low`, category=`other`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#10462** Combining image and data response in fast api.
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`medium`, category=`question`
  - Notes: (none)

- **#10717** FastAPI with Pydantic v2 and FastAPI-JWT-Auth
  - Human: severity=`high`, category=`bug`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#15448** Malformed Links in Documentation Home
  - Human: severity=`medium`, category=`documentation`
  - LLM: severity=`low`, category=`documentation`
  - Notes: (none)

- **#6007** Duplicate headers
  - Human: severity=`low`, category=`bug`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#5859** FastAPI==0.89.0 Cannot use `None` as a return type when `status_code` is set to 204 with `from __future__ import annotations`
  - Human: severity=`high`, category=`feature_request`
  - LLM: severity=`medium`, category=`bug`
  - Notes: (none)

- **#14444** FastAPI 0.123.5 breaks async wrappers using @wraps
  - Human: severity=`medium`, category=`other`
  - LLM: severity=`high`, category=`bug`
  - Notes: (none)
