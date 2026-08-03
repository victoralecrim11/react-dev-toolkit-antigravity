# React Native / Expo
Use junto de `./skills/react-dev/references/react-core.md` em apps móveis. Prefira Expo managed workflow, TypeScript, Expo Router e Hermes. Só recomende Bare Workflow se uma dependência nativa, integração de plataforma ou requisito de build não for suportado pelo Expo.

- Organize rotas no Expo Router; mantenha lógica de negócio fora das telas.
- Use Reanimated e Gesture Handler para animações/gestos fluidos, evitando atualizar estado React a cada frame.
- Considere offline, permissões, tamanhos de tela, inicialização e acessibilidade nativa.
- Valide em dispositivo físico quando recursos nativos forem envolvidos.

Explique por que uma dependência é necessária, a alternativa Expo e seu custo de manutenção.
