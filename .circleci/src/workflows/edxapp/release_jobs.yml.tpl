      # Run jobs for the ${RELEASE} release
      - ${RELEASE}:
          requires:
            - check-configuration
          filters:
            tags:
              ignore: /.*/
