```
  maadhav
  -------------------------------------------------
  models that run on the device, not in the cloud
```

### ai / ml engineer · on-device ai

hey, i'm maadhav. i build ml systems — small llms, vision models, rag — and get them running on real hardware: phone npus, arm boards, a car's own signals.
studying ece at kpriet, coimbatore. looking for ai/ml engineer and on-device ai internships.

### what i build

- **ml systems**: small llms, vision models, rag over real corpora, and evaluators that check whether an answer is right, not just similar.
- **on-device deployment**: quantized models on phone npus and arm boards. onnx runtime, llama.cpp / gguf, qualcomm ai hub / qnn, int8 / ptq.
- **embedded edge**: uart, spi, i²c, can / socketcan, lorawan, linux on the board.
- **optimisation**: milp dispatch for an edge energy controller.

### results

| event | result | year |
| --- | --- | --- |
| SEMICON India Hackathon, Applied Materials track | **runner-up (₹75,000)** | 2026 |
| Caterpillar Tech Challenge | **top 10 of ~1,500 teams**, grand finale | 2026 |
| Schneider Electric Yuva Yodha, challenge 3 | selected for phase 2 | 2026 |
| Arm × Bharat AI-SoC Challenge 2026–27 | shortlisted, team lead | 2026 |
| iQOO Hackathon | grand finale, 48-h build | 2026 |
| Qualcomm Snapdragon Multiverse Hackathon | selected for on-site build | 2026 |
| ISRO Bharatiya Antariksh Hackathon | grand finale shortlist | 2026 |
| Health-a-thon | top 150 of 450+ | 2026 |
| Atomic Hacks (IIT Bombay × Rosatom) | finalist | 2026 |
| Ossomehacks 2.0, SRM IST (Web3 track) | top 3 | 2025 |

### featured work

- **VehicleGPT**: offline small LLM over a car's CAN/VSS signals; 12 quantized models benchmarked on a 2-core, 2 GiB box; hybrid pipeline lifted accuracy 29.5% → 95.5%. Tata Elxsi Teliport S4. (code private until competition ends)
- **Rakshak-Edge**: offline scam SMS + URL detection on Arm, with a verifier that rejects unsupported explanations. Bharat AI-SoC, in progress. (code private until competition ends)
- **Mouna**: silent lip-reading to speech, offline on a phone NPU (PyTorch → ONNX → QNN); Kannada top-1 75.3%. iQOO Hackathon 2026 grand finale. (code private)
- **[semicon-driftsense](https://github.com/vhmaadhav/semicon-driftsense)**: finds a reference patch in an SEM wafer frame under unknown 8–12× zoom and ±5° rotation, or rejects it. siamese CNN F1 0.91. runner-up, SEMICON India 2026.
- **[embeddinggemma-mobile-benchmark](https://github.com/vhmaadhav/embeddinggemma-mobile-benchmark)**: EmbeddingGemma on Snapdragon phones via Qualcomm AI Hub, walked down a quantization ladder. in progress.
- **[hiver-email-suggested-response](https://github.com/vhmaadhav/hiver-email-suggested-response)**: retrieval-grounded LLM email replies, scored by a two-signal eval harness. 61.6 vs 11.4 for a copy-nearest-reply baseline, on 39 held-out examples.
- **Axiom Trace**: knowledge-graph RAG tutor for ECE with Bayesian mastery tracking and animated explanations; 176 tests. (code private for now)
- **DT Guardian**: edge controller for a 200 kVA transformer; MILP dispatch, −53% energy not served in a simulated outage. Schneider Yuva Yodha. (code private until competition ends)

### links

- site: [vhmaadhav.com](https://vhmaadhav.com)
- linkedin: [linkedin.com/in/vhmaadhav](https://linkedin.com/in/vhmaadhav)
- leetcode: [leetcode.com/u/vhmaadhav](https://leetcode.com/u/vhmaadhav/)
- email: [sid.maadhav@gmail.com](mailto:sid.maadhav@gmail.com)
