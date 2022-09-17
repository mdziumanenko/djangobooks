BEGIN;
--
-- Create model Book
--
CREATE TABLE "reviews_book" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(70) NOT NULL, "publication_date" date NOT NULL, "isbn" varchar(20) NOT NULL);
--
-- Create model Contributor
--
CREATE TABLE "reviews_contributor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_names" varchar(50) NOT NULL, "last_names" varchar(50) NOT NULL, "email" varchar(254) NOT NULL);
--
-- Create model Review
--
CREATE TABLE "reviews_review" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "rating" integer NOT NULL, "date_created" datetime NOT NULL, "date_edited" datetime NULL, "book_id" bigint NOT NULL REFERENCES "reviews_book" ("id") DEFERRABLE INITIALLY DEFERRED, "creator_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model BookContributor
--
CREATE TABLE "reviews_bookcontributor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "role" varchar(20) NOT NULL, "book_id" bigint NOT NULL REFERENCES "reviews_book" ("id") DEFERRABLE INITIALLY DEFERRED, "contributor_id" bigint NOT NULL REFERENCES "reviews_contributor" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field contributors to book
--
CREATE TABLE "new__reviews_book" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(70) NOT NULL, "publication_date" date NOT NULL, "isbn" varchar(20) NOT NULL);
INSERT INTO "new__reviews_book" ("id", "title", "publication_date", "isbn") SELECT "id", "title", "publication_date", "isbn" FROM "reviews_book";
DROP TABLE "reviews_book";
ALTER TABLE "new__reviews_book" RENAME TO "reviews_book";
CREATE INDEX "reviews_review_book_id_9a657eea" ON "reviews_review" ("book_id");
CREATE INDEX "reviews_review_creator_id_46914a15" ON "reviews_review" ("creator_id");
CREATE INDEX "reviews_bookcontributor_book_id_e7bfc5b2" ON "reviews_bookcontributor" ("book_id");
CREATE INDEX "reviews_bookcontributor_contributor_id_e3ee3341" ON "reviews_bookcontributor" ("contributor_id");
--
-- Add field publisher to book
--
CREATE TABLE "new__reviews_book" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(70) NOT NULL, "publication_date" date NOT NULL, "isbn" varchar(20) NOT NULL, "publisher_id" bigint NOT NULL REFERENCES "reviews_publisher" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__reviews_book" ("id", "title", "publication_date", "isbn", "publisher_id") SELECT "id", "title", "publication_date", "isbn", NULL FROM "reviews_book";
DROP TABLE "reviews_book";
ALTER TABLE "new__reviews_book" RENAME TO "reviews_book";
CREATE INDEX "reviews_book_publisher_id_a3cbe35c" ON "reviews_book" ("publisher_id");
COMMIT;
