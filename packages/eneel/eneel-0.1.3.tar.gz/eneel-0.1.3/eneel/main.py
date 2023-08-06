import eneel.load_runner as load_runner
import argparse
from pkg_resources import get_distribution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project", help="The name of the project (i.e my_project for project.yml)"
    )
    parser.add_argument(
        "--connections", help="Optionally add the full path to connections.yml"
    )
    parser.add_argument("--target", help="Optionally add the target. I.e prod")
    #    parser.add_argument('--logdir', help='For not using the default log directory')
    args = parser.parse_args()

    if not args.project:
        print(
            "You need to supply your project name. I.e my_project to use my_project.yml"
        )

    else:
        project_name = args.project
        if args.connections:
            connections = args.connections
        else:
            connections = None
        if args.target:
            target = args.target
        else:
            target = None
        import eneel.logger as logger

        logger = logger.get_logger(project_name)
        import eneel.printer as printer

        printer.print_msg("")
        printer.print_msg("Running eneel " +get_distribution('eneel').version)
        printer.print_msg("")
        logger.debug("Loading project: " + project_name)
        try:
            load_runner.run_project(
                project_name, connections_path=connections, target=target
            )
        except KeyboardInterrupt:
            print("Interupted by user")


if __name__ == "__main__":
    main()
