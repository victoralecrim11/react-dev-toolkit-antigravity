const fs = require('fs');
const path = require('path');

/**
 * Subagent Runtime - Real
 * Lê os arquivos agent.md do repositório e os converte em configurações
 * prontas para o framework agentico (Antigravity ou outro orchestrator).
 */
function loadSubagents(agentsDir) {
  const agents = [];
  
  if (!fs.existsSync(agentsDir)) {
    return agents;
  }
  
  const folders = fs.readdirSync(agentsDir);
  for (const folder of folders) {
    const agentPath = path.join(agentsDir, folder, 'agent.md');
    if (fs.existsSync(agentPath)) {
      const content = fs.readFileSync(agentPath, 'utf8');
      const parsed = parseAgent(content);
      if (parsed) {
        agents.push({
          id: folder,
          ...parsed
        });
      }
    }
  }
  
  return agents;
}

function parseAgent(content) {
  if (!content.startsWith('---\n')) {
    return null;
  }
  
  const endIdx = content.indexOf('\n---', 4);
  if (endIdx === -1) {
    return null;
  }
  
  const frontmatterRaw = content.substring(4, endIdx);
  const prompt = content.substring(endIdx + 4).trim();
  
  const frontmatter = {};
  let currentKey = null;
  
  for (let line of frontmatterRaw.split('\n')) {
    line = line.trimEnd();
    if (!line || line.trim().startsWith('#')) continue;
    
    if (line.startsWith(' ') && currentKey) {
      const val = line.trim();
      if (val.startsWith('-')) {
        if (!Array.isArray(frontmatter[currentKey])) {
          frontmatter[currentKey] = [];
        }
        frontmatter[currentKey].push(val.substring(1).trim());
      }
      continue;
    }
    
    if (line.includes(':')) {
      const [key, ...rest] = line.split(':');
      currentKey = key.trim();
      const val = rest.join(':').trim();
      
      if (val) {
        if (val === 'true') frontmatter[currentKey] = true;
        else if (val === 'false') frontmatter[currentKey] = false;
        else frontmatter[currentKey] = val;
      } else {
        frontmatter[currentKey] = [];
      }
    }
  }
  
  return {
    name: frontmatter.name,
    description: frontmatter.description,
    tools: frontmatter.tools || [],
    system_prompt: prompt
  };
}

module.exports = {
  loadSubagents,
  parseAgent
};
