# React Native / Expo
Use junto de `${CLAUDE_PLUGIN_ROOT}/skills/react-dev/references/react-core.md` em apps móveis. Prefira Expo managed workflow, TypeScript, Expo Router e Hermes. Só recomende Bare Workflow se uma dependência nativa, integração de plataforma ou requisito de build não for suportado pelo Expo.

- Organize rotas no Expo Router; mantenha lógica de negócio fora das telas.
- Use Reanimated e Gesture Handler para animações/gestos fluidos, evitando atualizar estado React a cada frame.
- Use `View`, `Text`, `Image`, `FlatList` e Flexbox como base de UI. Otimize listas longas com `FlatList` antes de criar abstrações próprias.
- Escolha persistência pelo problema: AsyncStorage para chave-valor simples, SQLite para dados relacionais locais, Realm quando objetos complexos e volume local justificarem, e backend remoto quando houver sincronização entre dispositivos.
- Encapsule persistência e APIs em repositories/services. Nunca manipule banco ou HTTP diretamente em componentes de UI.
- Implemente estados de loading, error e success em fluxos remotos; considere offline-first quando o produto precisa funcionar sem rede.
- Proteja credenciais com variáveis de ambiente e mecanismos seguros da plataforma. Não versione chaves de API.
- Considere offline, permissões, tamanhos de tela, inicialização e acessibilidade nativa.
- Valide em dispositivo físico quando recursos nativos forem envolvidos.

Explique por que uma dependência é necessária, a alternativa Expo e seu custo de manutenção.
