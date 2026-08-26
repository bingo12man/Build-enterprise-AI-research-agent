class ResearchAgentError(Exception):
    """Base exception for application errors."""


class RetrievalError(ResearchAgentError):
    """Raised when evidence retrieval fails."""


class LLMServiceError(ResearchAgentError):
    """Raised when LLM generation fails."""


class ValidationError(ResearchAgentError):
    """Raised when generated output fails validation."""