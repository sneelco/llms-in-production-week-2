import time

import guardrails as gd
import openai
import streamlit as st

from src.cached_resources import get_guard, get_guard_dynamodb, get_exact_match_cache, get_semantic_cache
from src.constants import OPENAI_MODEL_ARGUMENTS
from src.models import LLMResponse, LLMResponseDynamoDB

from redis import Redis
from redisvl.extensions.llmcache import SemanticCache

st.set_page_config(page_title="SQL Code Generator")
st.title("SQL Code Generator")


def generate_response(
        generation_type: str,
        input_text: str, 
        guard: gd.Guard,
        cache: SemanticCache | Redis,
        distance_threshold: float | None,
        cache_strategy: str
    ) -> None:
    """
    Generate a response for the given input text taking in the cache and guard.
    """
    try:
        start_time = time.time()
        cache_key = f"{generation_type}:{input_text}"

        if cache_strategy == "Semantic Cache":
            # Check the semantic cache for a semantically similar entry with the selected distance threshold
            cached_result = cache.check(
                prompt=cache_key, distance_threshold=distance_threshold
            )
        else:
            # Check the exact match cache using a simple Redis Hash lookup
            cached_result = cache.get(cache_key)
            if cached_result:
                cached_result = [{"response": cached_result.decode("utf-8")}]

        # If no cached result is found (cache miss)
        if not cached_result:
            (
                _,
                validated_response,
                _,
                validation_passed,
                error,
            ) = guard(
                openai.chat.completions.create,
                prompt_params={
                    "query": input_text,
                },
                **OPENAI_MODEL_ARGUMENTS,
            )
            total_time = time.time() - start_time
            if error or not validation_passed or not validated_response:
                st.error(f"Unable to produce an answer due to: {error}")
            elif generation_type == "DynamoDB":
                valid_dynamo = LLMResponseDynamoDB(**validated_response)
                generated_result = valid_dynamo.generated_query
            elif generation_type == "SQL":
                valid_sql = LLMResponse(**validated_response)
                generated_result = valid_sql.generated_sql
            else:
                st.error("Invalid Language detected")
                raise Exception("Invalid Language detected")

            st.text_area(label="Result", value=generated_result, disabled=True)
            st.info(f"That query took: {total_time:.2f}s")

            # Store the result in the appropriate cache for future use
            if cache_strategy == "Semantic Cache":
                cache.store(
                    prompt=cache_key,
                    response=generated_result,
                    # Metadata to track when the response was generated
                    metadata={"generated_at": time.time()},
                )
            else:
                cache.set(cache_key, generated_result)

        # If a cached result is found (cache hit)
        else:
            total_time = (
                time.time() - start_time
            )  # Calculate the total time taken to retrieve from cache
            st.text_area(label="Result", value=cached_result[0]["response"], disabled=True)
            st.info(f"That query took: {total_time:.2f}s")  # Display the time taken

    except Exception as e:
        st.error(f"Error: {e}")


def main() -> None:

    cache_strategy = st.radio(
        "Select cache strategy:", ("Exact Match Cache", "Semantic Cache")
    )

    if cache_strategy == "Semantic Cache":
        distance_threshold = st.slider(
            "Select distance threshold for semantic cache:",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01,
        )
    else:
        distance_threshold = None

    cache = (
        get_semantic_cache()
        if cache_strategy == "Semantic Cache"
        else get_exact_match_cache()
    )  # Initialize cache based on strategy

    with st.form("my_form"):
        generation_type = st.radio(
            "Select Language Type:", ("SQL", "DynamoDB")
        )
        
        if generation_type == "DynamoDB":
            guard = get_guard_dynamodb()
        elif generation_type == "SQL":
            guard = get_guard()
        else:
            st.error("Invalid Language Type")
            return
    
        st.warning("Our agent isn't perfect, it may not always produce acurate results.", icon="⚠️")
        text = st.text_area(
            "Enter text:",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            generate_response(generation_type, text, guard, cache, distance_threshold, cache_strategy)


if __name__ == "__main__":
    main()
