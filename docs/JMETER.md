# JMeter operational guidance

Sources checked 17 October 2026: Apache [getting started/CLI](https://jmeter.apache.org/usermanual/get-started.html), [best practices](https://jmeter.apache.org/usermanual/best-practices.html), [component reference](https://jmeter.apache.org/usermanual/component_reference.html), [dashboard](https://jmeter.apache.org/usermanual/generating-dashboard.html). Preserve the project's installed version, supported Java and plugins; do not install/update them without setup approval. No official JMeter MCP server is assumed.

## Inspect before running

Inventory JMX, included plans, custom samplers/JARs, Java/plugin versions, properties, thread groups, timers, assertions, preprocessors/extractors, CSV datasets, listeners and result save configuration. Inspect XML as data before executing a plan: JSR223 and plugins can execute code. Keep secrets in approved runtime sources, not JMX, checked-in CSV, command arguments or chat. Verify CSV sharing mode, recycle/EOF behavior, delimiter/encoding and unique data ownership for concurrent/distributed injectors. Align data files and plugin versions across approved injectors.

Correlate dynamic tokens/IDs and cookies per session, validate response/business success, and distinguish closed threads from an arrival-rate model supplied by a verified component. Do not claim exact arrival-rate execution from thread count alone. Check pacing/think time, warmup, transaction mix, generator limits and property overrides. JMeter HTTP samplers operate at protocol level and do not execute page JavaScript; a real-browser requirement needs a separately approved dedicated spawned browser runner.

## Run and stop

Use non-GUI execution for load. Disable expensive debug listeners such as View Results Tree for load runs; retain required assertions and minimal JTL fields. Resolve approved properties, JMX path and unique output directories first. Example shape for the selected authorized profile:

```sh
jmeter -n -t "/approved/plan.jmx" -q "/approved/nonsecret.properties" -l "/new/run/results.jtl" -j "/new/run/jmeter.log" -e -o "/new/run/dashboard"
```

The dashboard output must be empty or nonexistent; do not delete another run to satisfy it. The command is an execution example, not authorization. Never launch with placeholder targets or unrestricted default load. For user-run fallback provide the actual reviewed command and approved profile ID, request the sanitized summary/log errors and bounded JTL aggregate output, and record that execution was user-reported.

JMeter CLI completion alone does not enforce approved business SLOs or show that a load test passed. Map thresholds to actual post-run evaluation and abort conditions to verified runner/external control or a named, approved manual stop procedure with observation cadence. If real-time stop cannot meet the requested protection, block the run until resolved. Use readiness preflight with the unchanged profile digest; the helper checks declared mappings, not actual behavior. Confirm the installed release's graceful shutdown mechanism and target only this run; do not kill unrelated Java processes. Stop within approved scope and preserve aborted/partial samples.

## Analyze outputs

Confirm JTL save configuration/schema before parsing CSV/XML. Preserve timeStamp origin/timezone and elapsed, latency and connect timing semantics (milliseconds in standard sample fields); these are different boundaries. Inspect success, responseCode, label, thread counts, bytes and sample/error counts where present. Transaction Controller parent samples and children can double count; decide the reporting denominator. Retain failures/timeouts, sample counts, warmup exclusions, missing rows and injector saturation. Distributed tests need injector identity/clock and data/version parity. Do not sum throughput across incompatible windows or average percentiles. Record dashboard filters, percentile configuration and APDEX thresholds. Mark missing criteria or truncated JTL inconclusive.

## Local versus live validation

Local source checks and synthetic evidence tests do not validate an arbitrary JMX, plugin, target or load ceiling. A one-user smoke run still requires the approved target/profile and may have external effects. Later acceptance should cover a harmless fixture, business assertions, data isolation, stop handling, JTL/report consistency and injector limits. No target traffic is required merely to install this skill.
