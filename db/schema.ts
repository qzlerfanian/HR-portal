import { sql } from "drizzle-orm";
import { index, integer, real, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const jobs = sqliteTable("jobs", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  department: text("department").notNull().default("منابع انسانی"),
  location: text("location").notNull().default("تهران"),
  employmentType: text("employment_type").notNull().default("تمام‌وقت"),
  description: text("description").notNull(),
  requirements: text("requirements").notNull().default("[]"),
  status: text("status").notNull().default("published"),
  createdAt: text("created_at").notNull().default(sql`CURRENT_TIMESTAMP`),
}, (table) => [index("jobs_status_created_idx").on(table.status, table.createdAt)]);

export const applications = sqliteTable("applications", {
  id: text("id").primaryKey(),
  jobId: text("job_id").notNull().references(() => jobs.id),
  name: text("name").notNull(),
  email: text("email").notNull(),
  phone: text("phone").notNull(),
  resumeKey: text("resume_key").notNull(),
  score: real("score"),
  rationale: text("rationale"),
  strengths: text("strengths").notNull().default("[]"),
  gaps: text("gaps").notNull().default("[]"),
  consent: integer("consent", { mode: "boolean" }).notNull().default(false),
  status: text("status").notNull().default("new"),
  createdAt: text("created_at").notNull().default(sql`CURRENT_TIMESTAMP`),
}, (table) => [index("applications_job_score_idx").on(table.jobId, table.score)]);
