# About
This repository is an implementation of Amazon's Item-to-item Collaborative
Filtering recommendation system coupled with a theoretical model for limiting
influence in recommendation systems

## Sources
[Amazon's Item-to-item Collaborative Filtering](https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf)

[The Influence Limiter: Provably Manipulation-Resistant
Recommender Systems](https://presnick.people.si.umich.edu/papers/recsys07/p25-resnick.pdf)

# Data sources
This has been tested with the a minified set of Book-Crossing data available at
http://www2.informatik.uni-freiburg.de/~cziegler/BX/

# Requirements
The server running the build needs the following modules installed:
- docker

The server running the build also needs the pip requirements listed in
requirements/build_requirements.txt.

- Change loading optional data to be API driven, then add tests for that
