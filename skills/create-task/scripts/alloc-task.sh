#!/usr/bin/env sh
# alloc-task.sh — allocate the next task number behind a mutex and place a task file.
#
# The plain "max existing number + 1" scan races: two sessions creating a task at
# the same time both read the same max and both write the same number (with
# different slugs). This serialises the read-max / allocate / write critical
# section behind an atomic `mkdir` mutex, so the number can never collide.
#
# Scope: only closes the race when both sessions share one filesystem checkout of
# the task store. Separate clones/worktrees that converge via git still need
# git-side reconciliation — a local lock cannot help there.
#
# Usage:
#   alloc-task.sh --dir <tasksDir> --slug <slug> --from <file>
#
#   --dir    task store directory (required; the caller supplies it — this script
#            holds no default so it stays project-agnostic)
#   --slug   kebab-case slug for the filename (required)
#   --from   the already-written task file to move into place (required; on another
#            filesystem the move degrades to copy-then-unlink, so it is not atomic —
#            the mutex, not the move, is what makes the number safe)
#
# Prints the allocated basename to stdout, e.g. `104-add-widget.md`. The number is
# `${name%-<slug>.md}`. Non-zero on failure.
#
# Epic sub-tasks (`NNN.MM-slug.md`) are not handled here: they're usually created
# within a single session, so they don't race.

dir=
slug=
from=

while [ $# -gt 0 ]; do
  case "$1" in
    --slug) slug=$2 ;;
    --from) from=$2 ;;
    --dir)  dir=$2  ;;
    *) printf 'alloc-task: unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
  # `shift 2` is a no-op when the flag has no value, which would spin forever
  [ $# -ge 2 ] || { printf 'alloc-task: %s is missing its value\n' "$1" >&2; exit 2; }
  shift 2
done

[ -n "$dir" ]  || { printf 'alloc-task: --dir is required\n' >&2; exit 2; }
[ -n "$slug" ] || { printf 'alloc-task: --slug is required\n' >&2; exit 2; }
[ -n "$from" ] || { printf 'alloc-task: --from is required\n' >&2; exit 2; }
[ -f "$from" ] || { printf 'alloc-task: --from file not found: %s\n' "$from" >&2; exit 2; }

mkdir -p "$dir" || exit 1
lock="$dir/.alloc.lock"

# --- mtime accessor, resolved once: BSD stat wants -f, GNU wants -c. Probe on
#     digits, not exit status: GNU's -f is --file-system and can exit 0 anyway. ---
if [ -n "$(stat -f %m . 2>/dev/null | tr -cd 0-9)" ]; then
  mtime() { stat -f %m "$1"; }
else
  mtime() { stat -c %Y "$1"; }
fi

# --- acquire the mutex: atomic mkdir, break locks left stale (>15s) by a crash.
#     Staleness reads the lock dir's own mtime, so the dir stays empty — git cannot
#     track an empty dir, so a crashed run survives a consuming repo's `git add -A`
#     without leaving a committed turd. Don't reintroduce a file in here. ---
tries=0
while ! mkdir "$lock" 2>/dev/null; do
  now=$(date +%s)
  held=$(mtime "$lock" 2>/dev/null) || held=$now   # vanished => retry the mkdir
  if [ $((now - held)) -gt 15 ]; then
    rmdir "$lock" 2>/dev/null
    continue
  fi
  tries=$((tries + 1))
  [ "$tries" -gt 300 ] && { printf 'alloc-task: timed out acquiring %s\n' "$lock" >&2; exit 1; }
  sleep 0.1
done
trap 'rmdir "$lock" 2>/dev/null' EXIT INT TERM

# --- allocate the number inside the critical section. Leading digits cover epic
#     bases too (e.g. 012.03-foo.md => 12), so a new task never reuses one. ---
max=0
for f in "$dir"/*.md; do
  [ -e "$f" ] || continue
  n=$(basename "$f" | sed -n 's/^\([0-9]\{1,\}\).*/\1/p')
  [ -n "$n" ] || continue
  n=$(printf '%s' "$n" | sed 's/^0*//'); [ -n "$n" ] || n=0
  [ "$n" -gt "$max" ] && max=$n
done
name="$(printf '%03d' "$((max + 1))")-$slug.md"

# --- place the file while still holding the lock, so the number is durably claimed ---
mv "$from" "$dir/$name" || exit 1

printf '%s\n' "$name"
