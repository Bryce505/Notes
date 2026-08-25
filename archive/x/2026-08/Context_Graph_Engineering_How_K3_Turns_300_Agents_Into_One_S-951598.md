# Context Graph Engineering: How K3 Turns 300 Agents Into One Second Brain

- 原文链接：https://x.com/0xMortyx/status/2091868687493951598
- 作者：Morty @0xMortyx
- 发布时间：2026-08-24
- 剪藏时间：2026-08-25 18:15

---

You launch 300 agents at a research problem. Twenty minutes later they're all done. You now have a new problem: 300 separate answers, sitting in 300 separate boxes, and no idea how any of them relate.

Follow my Substack to get fresh AI alpha: substack.com/@0xMortyx

That's the part almost nobody talks about when they show off a big agent count. Running 300 agents in parallel is the easy half. The hard half is what a human analyst actually does with 300 findings: notice that two companies share a supplier, that one regulation touches half the list, that a single vendor sits underneath a dozen "independent" answers. That connecting work is the actual value, and it's exactly the part a pile of unrelated outputs throws away.

[图片]

Kimi K3's Agent Swarm is built to not throw it away. I'll call the layer that does this a context graph: my own term for what the orchestrator is doing under the hood, not an official Moonshot product name, but it's the clearest way to describe what actually makes this different from "run a bunch of agents and paste the outputs together." The end result, when it works, functions like a second brain built from 300 parallel searches instead of your own years of notes: something that already knows how its own pieces relate.

[图片]

What's official vs what's framing:Kimi Agent Swarm is a real, shipped Moonshot AI feature: an orchestrator that decomposes a task, dynamically spins up sub-agents with no predefined roles, runs them in parallel, and stitches the results into one deliverable. On K3 it scales to roughly 300 sub-agents across ~4,000 coordinated steps. "Context graph" is how I'm choosing to describe that stitching layer, not a term Moonshot uses.

[图片]

[图片]

What Agent Swarm Actually Does

No predefined roles, no hand-written workflow. The orchestrator decides the shape of the team itself.

THE REAL MECHANISM

Most multi-agent setups make you define the roles up front: a researcher, a writer, a checker, wired together by hand. Agent Swarm works differently. You give it one task, and an orchestrator reads the request, decides how it splits, and dynamically creates however many sub-agents the job actually needs, without you defining a single role in advance. Moonshot describes it as the AI designing its own organization chart for each job.

Each sub-agent runs independently, in parallel, on its own slice of the problem. The orchestrator doesn't do the research itself, it delegates, checks what comes back, and assembles the final result, closer to a project manager than a team member. On K3, this scales to roughly 300 sub-agents coordinating across about 4,000 steps, a real jump from K2.5's 100 agents and ~1,500 steps at launch.

[图片]

✓ You describe the outcome. The orchestrator designs the team that gets there

[图片]

[图片]

The Part That's Actually Novel: It Learned When to Split

Deciding to parallelize isn't a hand-written rule here, it's a trained skill.

TRAINED, NOT TEMPLATED

Most multi-agent frameworks decide when to fan out with a rule someone wrote: "if the task has more than N independent parts, spawn agents." That's brittle, it either over-splits simple tasks or under-splits complex ones. Moonshot's technical documentation describes a different approach for Agent Swarm: the orchestrator's decomposition behavior is trained with reinforcement learning on orchestration traces, so judging whether and how to split a task is a learned skill the model improved at, not a static template bolted onto a prompt.

That distinction is the whole difference between a swarm that helps and one that just multiplies your bill. A templated splitter parallelizes everything it's told to, whether or not the task actually benefits. A trained orchestrator has seen enough examples of splits that helped and splits that didn't to make that call itself.

Why this matters practically:You don't have to tell the orchestrator how many agents to use, or even that it should parallelize at all. Describe the outcome and let it judge the shape. If you find yourself specifying agent counts by hand, you're fighting the part of the system that's supposed to do that judgment for you.

✓ The system decides whether to split at all, not just how, and it learned that judgment

[图片]

[图片]

Walking Through One Real Case

Moonshot's own demo: collecting 200-plus scattered essays into one usable set. Here's what that actually involves.

ONE CONCRETE EXAMPLE

Abstract descriptions of "wide tasks" are easy to nod along to and hard to picture. So take one of Moonshot's own reference cases: gathering every essay a prolific writer has published, scattered across a personal site, old blog platforms, and reposts, into one organized, deduplicated set.

Done by hand, that's a person opening dozens of tabs, checking each essay against ones already found, normalizing formatting, and building an index, hours of tedious, easy-to-get-wrong work. Done as a swarm: the orchestrator treats "find every essay" as the wide part (many independent sources to check in parallel) and reserves the judgment calls, is this a duplicate, which version is canonical, for a synthesis step at the end instead of splitting that part too.

[图片]

✓ Wide where it helps, single-threaded where judgment calls need to stay coherent

[图片]

The Shape of Work It's Actually For

A swarm earns its overhead on wide, repetitive work. It's the wrong tool for one deep, careful task.

WIDE, NOT DEEP

Moonshot's own canonical example is matching one CV against a hundred job listings at once, high volume, similar structure, genuinely parallel. Real demo cases follow the same shape: dispatching agents across 100 YouTube niches to build a comparison table, or collecting 200-plus scattered essays into one organized set. The work is wide. Nobody's demoing a swarm writing one careful essay, because that's not what it's for.

If your task is one thing you need to think through carefully, in sequence, a swarm just adds coordination overhead on top of a job that was never parallel to begin with. Ask the "wide or deep" question before you reach for it.

The honest cost:Swarm tasks consume meaningfully more credits than a regular agent task, several times as much, depending on task complexity and how many sub-agents get spun up. Save it for jobs where 300 parallel angles are actually worth paying for.

✓ Wide and repetitive: reach for the swarm. One careful task: use one agent.

[图片]

[图片]

What a Swarm Actually Costs You

300 agents don't run for free. Know the trade before you reach for the biggest number.

THE PRICE OF WIDTH

An Agent Swarm task consumes meaningfully more credits than a regular agent task, several times as much by Moonshot's own framing, scaling with task complexity and how many sub-agents actually get spun up. That's not a hidden cost, it's the direct consequence of running dozens or hundreds of models instead of one. The question worth asking before every swarm run isn't "can this be parallelized," it's "is the time saved worth several times the spend."

For a genuinely wide task, that trade is usually easy: an hour of a person's time checking 100 sources by hand costs more than the credits do. For a task that only looks wide, five sub-questions that were really one question in disguise, the swarm is just an expensive way to arrive at the same answer a single well-prompted agent would have given you.

A quick gut-check before you launch one:Could a single agent, given the same prompt, actually do this in one careful pass without missing anything? If yes, you don't need the swarm, you need a better single prompt. Save Agent Swarm for tasks where the honest answer is no.

✓ Width costs real credits. Spend them on tasks where width is the actual bottleneck.

[图片]

[图片]

What's Real, at a Glance

[图片]

The honest takeaway:300 agents finishing fast was never the impressive part, that's just parallelism. What's actually worth paying attention to is that nobody had to design the team by hand, and the output comes back as one usable thing instead of 300 tabs you have to reconcile yourself. Call that a context graph or call it something else, the mechanism is what matters.
