# Automated Software Engineering - Notizen

## AutoGen
- Ollama supported by default
    - ChatCompletionClient required for creating agents
- Can create custom Agents
- Try different communications
    - Does they differ in performance?
    - Does Team differ from Solo-Agent?
        - Prove that single agent is inadequate
- AssistantAgent provides tools
    - e.g. web-search
    - could imagine of syntax-checking, ! Check for commons errors and what information could reduce the error
- Context can be selected (i.e. the whole history convo or solely the last n messages)
- Can it operate on local files?
- Git checkout, wie am besten?
- Wollte immer eigene Tests schreiben und ausführen

- Single-Agent-Approach schnell an Grenzen
    - Seperation of concerns verletzt
- Multi-Agent approach
    - FileSurfer performance abh. von Sprachmodell
- MagenticOne als Coding assistant bereits vorhanden
- Doku für Agenten nicht gut; solo-testing für einige Agenten -
- Chain-Of-Thought durch Random Communication
- Daten-Weitergabe in Verantwortung des LLMs
- Manchmal falsche File-Referenz
- Zeigen der Dir structure zum finden der korrekten Datei

### Variations
- Used LLM
- Used Prompt
- Single/Multi-Agent