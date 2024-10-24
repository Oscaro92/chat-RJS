from agent import AgentRJS

agent = AgentRJS()

urls = ["https://cdn.1j1ju.com/medias/ee/b8/88-skyjo-regle.pdf", "https://cdn.1j1ju.com/medias/bd/ad/a7-7-wonders-duel-regles.pdf", "https://cdn.1j1ju.com/medias/c1/43/b7-schotten-totten-regle.pdf", "https://cdn.1j1ju.com/medias/ce/c4/60-7-wonders-regle.pdf", "https://images-fr-cdn.asmodee.com/eu-central-1/filer_public/92/3b/923b1bbc-0f39-466c-836f-9e33d911c291/dobb01fr_rules_lr.pdf", "https://www.jeuxdujardin.fr/files/regles/rdj-mb-classique-poche-et-pegbo---ok.pdf"]

for url in urls:
    print(f"import {url}")
    docs = agent.loadDoc(url)

    agent.saveDoc(docs)