from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from rag_helper import RAGBase
from sqlite_helper import SQLiteSpanExporter

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter('traces.db'))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")

class RAGTraced(RAGBase):
    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)

    def search(self, query):
        with tracer.start_as_current_span("search"):
            return super().search(query)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            llm_results = super().llm(prompt)
            span.set_attribute("input_tokens", llm_results.usage.input_tokens)
            span.set_attribute("output_tokens", llm_results.usage.output_tokens)
            
            return llm_results

