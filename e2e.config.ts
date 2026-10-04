// ABOUTME: Exercises the real production Hugo site in one Chromium worker.
// ABOUTME: The runner owns a pinned Hugo server and keeps its output isolated.
import type { E2EConfig } from "e2e";
import { web } from "@e2e-dev/web";

export default {
  tests: "tests/e2e/**/*.e2e.ts",
  workers: 1,
  retries: 0,
  targets: [
    {
      engine: web(),
      app: {
        url: "http://127.0.0.1:23899",
        command: {
          executable: "mise",
          args: [
            "exec",
            "--",
            "hugo",
            "server",
            "--environment",
            "production",
            "--bind",
            "127.0.0.1",
            "--port",
            "23899",
            "--baseURL",
            "http://127.0.0.1:23899/",
            "--destination",
            ".e2e/site",
            "--disableLiveReload",
            "--disableFastRender",
            "--watch=false",
          ],
          env: { GOROOT: "" },
          startupTimeout: 600_000,
          log: ".e2e/logs/hugo.log",
        },
      },
    },
  ],
} satisfies E2EConfig;
