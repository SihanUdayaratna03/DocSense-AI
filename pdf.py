import os
import time
import shutil
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PDFReader


def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)

        # Use a smaller chunk size to reduce nodes per batch and avoid rate limits
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
        nodes = splitter.get_nodes_from_documents(data, show_progress=True)

        print(f"Total nodes to embed: {len(nodes)}")

        # Build index in small batches with delays to respect rate limits
        batch_size = 5
        all_embedded_nodes = []

        from llama_index.core import Settings

        for i in range(0, len(nodes), batch_size):
            batch = nodes[i : i + batch_size]
            print(f"Embedding nodes {i + 1}–{min(i + batch_size, len(nodes))} of {len(nodes)}...")
            try:
                texts = [node.get_content() for node in batch]
                embeddings = Settings.embed_model.get_text_embedding_batch(texts)
                for node, emb in zip(batch, embeddings):
                    node.embedding = emb
                all_embedded_nodes.extend(batch)
            except Exception as e:
                print(f"Error embedding batch {i}–{i + batch_size}: {e}")
                print("Waiting 60 seconds before retrying...")
                time.sleep(60)
                # Retry the same batch once
                try:
                    texts = [node.get_content() for node in batch]
                    embeddings = Settings.embed_model.get_text_embedding_batch(texts)
                    for node, emb in zip(batch, embeddings):
                        node.embedding = emb
                    all_embedded_nodes.extend(batch)
                except Exception as e2:
                    print(f"Retry failed for batch {i}: {e2}. Skipping batch.")

            # Pause between batches to stay within rate limits
            if i + batch_size < len(nodes):
                time.sleep(3)

        index = VectorStoreIndex(all_embedded_nodes)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


pdf_path = os.path.join("data", "Sri_Lanka.pdf")
sri_lanka_pdf = PDFReader().load_data(file=pdf_path)
sri_lanka_index = get_index(sri_lanka_pdf, "sri_lanka")
sri_lanka_engine = sri_lanka_index.as_query_engine()
