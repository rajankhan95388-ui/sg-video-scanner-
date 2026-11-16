# Policy snapshots checked 2026-11-16. Rule packs are intentionally separate.
PACKS = {
"youtube": {
 "version":"Page checked 2026-11-16; includes 2025-07-15 inauthentic-content clarification",
 "sources":[
  {"source_id":"yt_monetization","title":"YouTube channel monetization policies","url":"https://support.google.com/youtube/answer/1311392?hl=en","source_revision":"2025-07-15 clarification; checked 2026-11-16","checked_on":"2026-11-16","validation_status":"verified"},
  {"source_id":"yt_copyright","title":"Learn about copyright claims","url":"https://support.google.com/youtube/answer/6013276?hl=en","source_revision":"Live page; checked 2026-11-16","checked_on":"2026-11-16","validation_status":"verified"}],
 "rules":[
  {"id":"YT_REUSED_CONTENT","category":"originality_monetization","title":"Reused-content risk","signals":["third_party_visual_match","low_transformative_value"],"source_ids":["yt_monetization"],"human":True,"advice":["Identify third-party clips and sources.","Add meaningful original commentary, analysis or educational value; permission alone does not settle the reused-content assessment."]},
  {"id":"YT_INAUTHENTIC_CONTENT","category":"originality_monetization","title":"Inauthentic or mass-produced content risk","signals":["repetitive_template_signal"],"source_ids":["yt_monetization"],"human":True,"advice":["Make each upload materially distinct and useful to viewers."]},
  {"id":"YT_CONTENT_ID","category":"copyright","title":"Content ID match","signals":["licensed_fingerprint_match"],"source_ids":["yt_copyright"],"force_unverified":True,"advice":["Check YouTube Studio copyright details after upload.","Confirm rights for every audio and visual element."]}]},
"facebook": {
 "version":"Meta Community Standards page checked 2026-11-16; no semantic version",
 "sources":[
  {"source_id":"meta_standards","title":"Meta Safety Center — Community Standards","url":"https://www.meta.com/safety/topics/safety-basics/policies/","source_revision":"Undated live page; checked 2026-11-16","checked_on":"2026-11-16","validation_status":"verified"},
  {"source_id":"meta_monetization","title":"Meta monetization policy index","url":"https://transparency.meta.com/policies/monetization/","source_revision":"Content not validated in this run","checked_on":"2026-11-16","validation_status":"pending_validation"}],
 "rules":[
  {"id":"FB_COMMUNITY_STANDARDS","category":"community_guidelines","title":"Community Standards risk signals","signals":["community_safety_signal"],"source_ids":["meta_standards"],"human":True,"advice":["Review the flagged timestamp against the linked official policy and preserve context for human review."]},
  {"id":"FB_MONETIZATION","category":"monetization","title":"Content monetization eligibility","signals":["account_monetization_status"],"source_ids":["meta_monetization"],"force_unverified":True,"advice":["Check current Page/profile monetization status in Meta's own tools."]},
  {"id":"FB_RIGHTS_MANAGER","category":"copyright","title":"Meta rights matching","signals":["licensed_fingerprint_match"],"source_ids":["meta_standards"],"force_unverified":True,"advice":["Verify music and footage rights with the rights holder or a licensed provider."]}]},
"instagram": {
 "version":"Originality announcement dated 2024-04-30; sources checked 2026-11-16",
 "sources":[
  {"source_id":"ig_guidelines","title":"Instagram Community Guidelines","url":"https://help.instagram.com/477434105621119/","source_revision":"Content not validated in this run","checked_on":"2026-11-16","validation_status":"pending_validation"},
  {"source_id":"ig_originality","title":"Meta Newsroom (pt-BR) — Ajudando o criador de conteúdo a encontrar novos públicos","url":"https://about.fb.com/br/news/2024/04/ajudando-o-criador-de-conteudo-a-encontrar-novos-publicos/","source_revision":"Published 2024-04-30","checked_on":"2026-11-16","validation_status":"verified"}],
 "rules":[
  {"id":"IG_COMMUNITY_GUIDELINES","category":"community_guidelines","title":"Community Guidelines risk signals","signals":["community_safety_signal"],"source_ids":["ig_guidelines"],"human":True,"advice":["Review the flagged segment against the current Instagram Community Guidelines."]},
  {"id":"IG_ORIGINALITY","category":"recommendation_originality","title":"Originality and recommendation signals","signals":["visual_audio_duplicate_signal","repetitive_template_signal"],"source_ids":["ig_originality"],"human":True,"advice":["Use content you created or have rights to use.","Add material original commentary or creative transformation; this is not a copyright clearance test."]},
  {"id":"IG_ACCOUNT_ELIGIBILITY","category":"account_level_distribution","title":"Account recommendation eligibility","signals":["account_recommendation_status"],"source_ids":["ig_originality"],"force_unverified":True,"advice":["Check Account Status inside Instagram; this scanner does not access account data."]},
  {"id":"IG_COPYRIGHT","category":"copyright","title":"Instagram copyright matching","signals":["licensed_fingerprint_match"],"source_ids":["ig_guidelines"],"force_unverified":True,"advice":["Verify licenses for music, clips, images and other third-party material."]}]}
}

def evaluate(platform, signals):
    pack = PACKS[platform]
    by_kind = {}
    for s in signals:
        by_kind.setdefault(s.kind, []).append(s)
    findings = []
    for r in pack["rules"]:
        matches = [s for k in r["signals"] for s in by_kind.get(k, [])]
        evidence = [e for s in matches for e in s.evidence]
        confidence = max([s.confidence for s in matches if s.confidence is not None], default=None)
        if r.get("force_unverified"):
            status, note = "not_verified", "Requires account access or proprietary matching not connected here."
        elif not matches or all(s.status == "not_run" for s in matches):
            status, note = "not_run", "No configured adapter produced the required signal."
        elif any(s.status == "not_verified" for s in matches):
            status, note = "not_verified", "At least one required signal could not be verified."
        elif any(s.status == "detected" for s in matches):
            status, note = ("manual_review" if r.get("human") else "risk_detected"), "A model signal is not a final platform decision."
        elif all(s.status == "not_detected" for s in matches):
            status, note = ("manual_review" if r.get("human") else "pass"), "No signal detected does not establish platform approval."
        else:
            status, note = "not_verified", "Signal set is incomplete."
        findings.append({"finding_id":r["id"],"category":r["category"],"title":r["title"],
          "status":status,"severity":"unknown","confidence":confidence,
          "explanation":"Policy-based review signal; not an enforcement prediction.",
          "evidence":evidence,"remediation":r["advice"],"source_ids":r["source_ids"],"limitations":[note]})
    return findings
