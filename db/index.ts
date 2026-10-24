import { env } from "cloudflare:workers";
import { drizzle } from "drizzle-orm/d1";
import * as schema from "./schema";

export function getDb() {
  if (!env.DB) {
    throw new Error(
      "Cloudflare D1 binding `DB` is unavailable. Set the `d1` field in .openai/hosting.json to `DB` or let your control plane inject the real binding values before using the database."
    );
  }

  return drizzle(env.DB, { schema });
}

let schemaReady: Promise<void> | undefined;

/** Creates the small app schema on first use so a fresh D1 binding is ready immediately. */
export async function ensureDatabaseSchema() {
  if (!env.DB) throw new Error("Cloudflare D1 binding `DB` is unavailable.");
  schemaReady ??= (async () => {
    const statements = [
      `CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY NOT NULL, title TEXT NOT NULL, department TEXT NOT NULL DEFAULT 'منابع انسانی', location TEXT NOT NULL DEFAULT 'تهران', employment_type TEXT NOT NULL DEFAULT 'تمام‌وقت', description TEXT NOT NULL, requirements TEXT NOT NULL DEFAULT '[]', status TEXT NOT NULL DEFAULT 'published', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)`,
      `CREATE TABLE IF NOT EXISTS applications (id TEXT PRIMARY KEY NOT NULL, job_id TEXT NOT NULL, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, resume_key TEXT NOT NULL, score REAL, rationale TEXT, strengths TEXT NOT NULL DEFAULT '[]', gaps TEXT NOT NULL DEFAULT '[]', consent INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'new', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(job_id) REFERENCES jobs(id))`,
      `CREATE INDEX IF NOT EXISTS jobs_status_created_idx ON jobs(status, created_at)`,
      `CREATE INDEX IF NOT EXISTS applications_job_score_idx ON applications(job_id, score)`,
    ];
    for (const statement of statements) await env.DB!.prepare(statement).run();
  })().catch((error) => { schemaReady = undefined; throw error; });
  await schemaReady;
}
