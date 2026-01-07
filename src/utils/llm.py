"""
LLM integration utilities for generating realistic text content.
Optional - uses OpenAI API if available and configured.
"""
import os


def get_openai_client():
    """Get OpenAI client if available and configured."""
    try:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your-api-key-here":
            return OpenAI(api_key=api_key)
    except ImportError:
        pass
    return None


def generate_task_names_with_llm(department, project_type, count=10):
    """
    Use OpenAI to generate realistic task names.
    Returns None if LLM is not available.
    """
    client = get_openai_client()
    if not client:
        return None
    
    try:
        prompt = f"""Generate {count} realistic task names for a {department} team 
working on a {project_type} project at a B2B SaaS company.
Return only the task names, one per line. Make them specific and realistic."""
        
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8
        )
        names = response.choices[0].message.content.strip().split('\n')
        return [n.strip().lstrip('0123456789.-) ') for n in names if n.strip()]
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None
