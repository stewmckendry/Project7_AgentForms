# 🧠 Function Interface Spec

## `src/src/client/app.py`
### `ask_next() -> Unknown`
> No description provided.

## `src/src/models/agent/followup_generator.py`
### `generate_followups_from_responses(finalized_responses, strategy_path) -> Unknown`
> Generate follow-up questions based on finalized responses using strategy config.

> Args:
>     finalized_responses (dict): Final output from finalize_draft_responses
>     strategy_path (str): Path to question_strategy.yaml

> Returns:
>     list of follow-up dicts with question_id, followup_question, reason, importance

## `src/src/models/agent/followup_loop.py`
### `reparse_response(q_id, user_input, question_config) -> Dict`
> No description provided.

## `src/src/models/agent/followup_loop.py`
### `run_followup_loop(finalized_responses, question_config) -> Tuple[Dict, Dict]`
> No description provided.

## `src/src/models/agent/guidance_generator.py`
### `generate_guidance(responses) -> Unknown`
> No description provided.

## `src/src/models/agent/guidance_generator.py`
### `get_value(responses, key) -> Unknown`
> No description provided.

## `src/src/models/agent/rtp_qa.py`
### `generate_rtp_response_rule_based(activity_name, assessment_bundle, rtp_reference) -> Dict`
> No description provided.

## `src/src/models/agent/rtp_qa.py`
### `generate_rtp_response_llm(user_question, assessment_bundle, rtp_reference) -> dict`
> No description provided.

## `src/src/models/generate_guidance_v2.py`
### `generate_guidance(assessment_bundle) -> Dict`
> No description provided.

## `src/src/models/llm_analyze_freeform_input.py`
### `analyze_freeform_input(agent, user_input) -> Unknown`
> Analyze a free-form explanation and attempt to answer known assessment questions.

> Parameters:
> - user_input (str): the full narrative or situation description
> - known_questions (list of dict): each with {id, prompt, type}

> Returns:
> - dict with keys:
>     - 'draft_responses': dict keyed by question_id with {value, thought, certainty, parsed_by}
>     - 'summary_thought': overall explanation of what was extracted

## `src/src/models/llm_followups.py`
### `generate_followup_question(q_id, response, strategy_entry, all_responses) -> Unknown`
> Generate a follow-up question using the response, strategy entry, and optionally other context.

> Args:
>     q_id (str): The question ID (e.g., 'injury_date')
>     response (dict): Finalized response for this question
>     strategy_entry (dict): Info from question_strategy.yaml
>     all_responses (dict): All finalized responses (optional)

> Returns:
>     dict: {
>         question_id,
>         followup_question,
>         reason,
>         importance
>     }

## `src/src/models/llm_guidance.py`
### `generate_guidance(assessment_bundle) -> Dict`
> No description provided.

## `src/src/models/llm_openai.py`
### `call_openai_chat(system_prompt, user_prompt, model, temperature) -> Unknown`
> No description provided.

## `src/src/models/llm_responsevalidators.py`
### `llm_parse_date(input_text) -> Unknown`
> No description provided.

## `src/src/models/llm_responsevalidators.py`
### `llm_interpret_yes_no(input_text) -> Unknown`
> No description provided.

## `src/src/models/llm_responsevalidators.py`
### `llm_extract_symptoms(user_input, symptom_reference) -> Unknown`
> Extract and match symptoms using LLM, enriched with a known symptom reference.

## `src/src/models/llm_responsevalidators.py`
### `parse_with_fallback(input_text, type_hint) -> Unknown`
> No description provided.

## `src/src/models/llm_responsevalidators.py`
### `is_valid_date_string(date_str) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `ping() -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `analyze(req) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `finalize(req) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `followups(req) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `guidance(req) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `rtp(req) -> Unknown`
> No description provided.

## `src/src/server/main.py`
### `rtp_ask(req) -> Unknown`
> No description provided.

## `src/src/utils/logging/logger.py`
### `setup_logger(name, filename) -> Unknown`
> No description provided.

## `src/src/utils/output/exporter.py`
### `export_json(responses) -> Unknown`
> No description provided.

## `src/src/utils/output/exporter.py`
### `export_markdown(chat_history, guidance) -> Unknown`
> No description provided.

## `src/src/utils/output/followup_reporting.py`
### `build_followup_trace_report(agent, followups) -> Unknown`
> No description provided.

## `src/src/utils/processing/json_yaml_repair.py`
### `repair_json_like_string(s) -> str`
> Cleans LLM output to make it safe for json.loads().
> - Removes markdown code fences
> - Fixes trailing commas
> - Converts single quotes to double quotes
> - Normalizes true/false/null

## `src/src/utils/processing/json_yaml_repair.py`
### `repair_yaml_like_string(s) -> str`
> No description provided.

## `src/src/utils/processing/process_draft_response.py`
### `finalize_draft_responses(agent, symptom_reference) -> Unknown`
> No description provided.

## `src/src/utils/protocols/load_concussion_flow.py`
### `load_concussion_flow(path) -> Unknown`
> No description provided.

## `src/src/utils/protocols/load_question_strategy.py`
### `load_question_strategy(path) -> Unknown`
> No description provided.

## `src/src/utils/protocols/load_symptom_reference.py`
### `load_symptom_reference(path) -> Unknown`
> No description provided.

## `src/src/utils/protocols/load_symptom_reference.py`
### `match_symptoms(user_symptoms, reference) -> Unknown`
> No description provided.

## `src/src/utils/protocols/question_loader.py`
### `extract_question_list_from_yaml(yaml_path) -> Unknown`
> No description provided.

## `src/src/utils/protocols/rtp_utils.py`
### `find_current_stage(responses) -> str`
> Very basic rule-based logic to infer current RTP stage.
> Could be replaced later by LLM.

## `src/src/utils/protocols/rtp_utils.py`
### `summarize_bundle(assessment_bundle) -> str`
> Create a concise summary of key structured responses for LLM prompt context.

## `src/src/utils/protocols/rtp_utils.py`
### `summarize_rtp_protocol(rtp_reference) -> str`
> Formats a short readable version of the RTP protocol for inclusion in an LLM prompt.

## `src/src/utils/protocols/rtp_utils.py`
### `parse_llm_rtp_response(response_text) -> Dict`
> Parses the LLM markdown response into structured fields.
> Can be upgraded later with regex or JSON parsing.

## `src/src/utils/validation/response_validator.py`
### `parse_date(text) -> Unknown`
> No description provided.

## `src/src/utils/validation/response_validator.py`
### `parse_yes_no(text) -> Unknown`
> No description provided.

## `src/src/utils/validation/response_validator.py`
### `parse_symptoms(text) -> Unknown`
> No description provided.

## `test/test/test_agent_flow.py`
### `sample_agent() -> Unknown`
> No description provided.

## `test/test/test_agent_flow.py`
### `test_agent_runs_to_completion(sample_agent) -> Unknown`
> No description provided.

## `test/test/test_finalize_draft_responses.py`
### `mock_agent() -> Unknown`
> No description provided.

## `test/test/test_finalize_draft_responses.py`
### `test_finalize_responses_with_parsers(mock_extract_questions, mock_symptom_parser, mock_date_parser, mock_agent) -> Unknown`
> No description provided.