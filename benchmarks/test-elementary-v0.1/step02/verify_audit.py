from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parent;root=base.parents[2];spec=json.loads((base/'AUDIT_VERIFICATION.json').read_text())
checks=[]
def check(label,ok):
 checks.append({'check':label,'passed':bool(ok)})
 if not ok:raise AssertionError(label)
for path,want in spec['immutable_archive_sha256'].items():check('unchanged archive '+path,hashlib.sha256((root/path).read_bytes()).hexdigest()==want)
for name,want in spec['historical_protocol_sha256'].items():check('preserved historical '+name,hashlib.sha256((base/'historical'/name).read_bytes()).hexdigest()==want)
for name in ['MODEL_INPUT.md','NATURAL_PROMPT.md','GUIDED_PROMPT.md','MASKED_EVALUATOR_PROMPT.md']:
 s=(base/name).read_text();check('whole-department rule '+name,'Splitting any department across masses is prohibited' in s)
for name in ['QUALITY_PACKET.md','BEHAVIOR_PACKET.md']:
 s=(base/'results/batch-01/delivery'/name).read_text();ids=re.findall(r'^(?:# )?(R\d{2})\s*$',s,re.M);check('12 unique ordered records '+name,ids==['R%02d'%i for i in range(1,13)])
 bad=re.search(r'run_metadata|source document page|ChatGPT|Opus|Claude|Sonnet|Rhino|Worked for|Thought for|SHUFFLE_KEY|(?:condition|model|source.run|reasoning.setting)\s*:',s,re.I);check('no scanned direct metadata '+name,bad is None)
 if name=='QUALITY_PACKET.md':check('no search-rationale section '+name,not re.search(r'^stated_rationale$',s,re.M))
# Relative Markdown file links across all docs, excluding links and original archive citations outside repo.
for p in root.rglob('*.md'):
 if '/historical/' in str(p):continue
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  t=target.split('#')[0]
  if t:check('link '+str(p.relative_to(root))+' -> '+t,(p.parent/t).exists() or str((p.parent/t).resolve().relative_to(root.resolve())) in spec['existing_repository_paths'])
print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
