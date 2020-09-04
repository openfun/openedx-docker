  # Run jobs for the ${RELEASE} release
  ${RELEASE}:
    <<: [*defaults, *build_steps]
