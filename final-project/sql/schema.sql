PRAGMA foreign_keys = ON;

-- dimension tables
CREATE TABLE IF NOT EXISTS district(
  district_id TEXT PRIMARY KEY,
  name        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS school(
  school_id   TEXT PRIMARY KEY,
  district_id TEXT NOT NULL REFERENCES district(district_id),
  name        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subgroup(
  subgroup_code TEXT PRIMARY KEY,
  label         TEXT NOT NULL
);

-- facts
CREATE TABLE IF NOT EXISTS enrollment(
  year           INTEGER NOT NULL CHECK (year >= 2000),
  school_id      TEXT NOT NULL REFERENCES school(school_id),
  subgroup_code  TEXT NOT NULL REFERENCES subgroup(subgroup_code),
  number_students INTEGER NOT NULL CHECK (number_students >= 0),
  pct_students    REAL,
  PRIMARY KEY (year, school_id, subgroup_code)
);

CREATE TABLE IF NOT EXISTS attendance(
  year           INTEGER NOT NULL CHECK (year >= 2000),
  school_id      TEXT NOT NULL REFERENCES school(school_id),
  subgroup_code  TEXT NOT NULL REFERENCES subgroup(subgroup_code),
  attendance_indicator REAL,
  chronic_absent_rate  REAL,
  PRIMARY KEY (year, school_id, subgroup_code)
);

CREATE TABLE IF NOT EXISTS assessments(
  year           INTEGER NOT NULL CHECK (year >= 2000),
  school_id      TEXT NOT NULL REFERENCES school(school_id),
  subject        TEXT NOT NULL CHECK (subject IN ('ELA','MATH')),
  grade          INTEGER NOT NULL,
  subgroup_code  TEXT NOT NULL REFERENCES subgroup(subgroup_code),
  tested         INTEGER NOT NULL CHECK (tested >= 0),
  n_qual         INTEGER NOT NULL CHECK (n_qual >= 0),
  qual_rate      REAL,
  PRIMARY KEY (year, school_id, subject, grade, subgroup_code)
);
