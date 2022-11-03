# nd064_C1

## Hello!

I actually wrote something here.

Thanks for having a look.  I also included some run notes from the experience here.

### M1 Mac

I know that I was warned against it, but it was my most convenient machine, and I 
was comfortable enough with the material to give it a try.

I ended up completing this section on an M1 Mac.  Installing `podman` with Homebrew
and following the guidance of [this kind/podman](https://faun.dev/c/stories/nilesh93/replacing-docker-desktop-with-podman-and-kind-in-macos/) integration got me almost all
the way there.

During the argocd pieces, the default cluster size is a bit small to handle those
resource requirements, so I expanded the cluster size using the `small.yml` cluster
configuration you can see here.  In the end, I wasn't able to have techtrends staging
and production running at the same time, but they did start successfully from the
manifests in the `projects/argo` directory as directed.

I will also record this feedback in the real Udemy program, but since it did impact
some of my screenshots, I figured I'd share here as well.

### GitHub Actions

So with GitHub at this point moving to `buildx` and delivering the repository contents
to that process via an opaque process that can't really be influenced, I gave up and
copied the `Dockerfile` for techtrends into the project root, rather than outside the
project home entirely.

I feel this can be justified, but I suppose you'll be the judge!

I don't think it's the spirit of the exercise to figure out how exactly the GitHub build
action works, but you may feel differently.

I did include the standout build for some "extra credit" here.



### Cloud Native Fundamentals Scholarship Program Nanodegree Program

**Course Homepage**: https://sites.google.com/udacity.com/suse-cloud-native-foundations/home

**Instructor**: https://github.com/kgamanji
