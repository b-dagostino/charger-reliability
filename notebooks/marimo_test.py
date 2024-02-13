import marimo

__generated_with = "0.2.4"
app = marimo.App(width="full")


@app.cell
def __():
    from typing import Any

    import marimo as mo
    import pandas as pd
    return Any, mo, pd


@app.cell
def __(Any, mo):
    from kedro.framework.context import KedroContext
    from kedro.framework.session import KedroSession
    from kedro.io import DataCatalog


    def reload_kedro(
        path: str | None = None,
        env: str | None = None,
        extra_params: dict[str, Any] | None = None,
        local_namespace: dict[str, Any] | None = None,
        conf_source: str | None = None,
    ) -> tuple[KedroSession, KedroContext, DataCatalog, Any]:
        from kedro.ipython import (
            _resolve_project_path,
            _remove_cached_modules,
            configure_project,
        )
        from kedro.framework.startup import bootstrap_project

        from kedro.framework.project import pipelines

        project_path = _resolve_project_path(None, None)
        metadata = bootstrap_project(project_path)
        _remove_cached_modules(metadata.package_name)
        configure_project(metadata.package_name)

        session = KedroSession.create(project_path)
        context = session.load_context()
        catalog = context.catalog

        return (session, context, catalog, pipelines)

    session, context, catalog, pipelines = reload_kedro()
    session.run()
    mo.output.clear()
    return (
        DataCatalog,
        KedroContext,
        KedroSession,
        catalog,
        context,
        pipelines,
        reload_kedro,
        session,
    )


@app.cell
def __(mo, pipelines):
    datasets = set().union(*[pipeline.datasets() for pipeline in pipelines.values()])

    dataset_dropdown = mo.ui.dropdown(options=datasets)
    mo.md(f"""# Kedro Dataset
    {dataset_dropdown}""")
    return dataset_dropdown, datasets


@app.cell
def __(catalog, dataset_dropdown, mo, pd):
    if dataset_dropdown.value:
        dataset_df = catalog.load(dataset_dropdown.value)
        # convert categorical types to strings so marimo doesn't freak out
        # dataset_df = dataset_df.astype("object").convert_dtypes()
        with pd.option_context('display.max_rows', 100, 'display.max_columns', None): 
            mo.output.replace(dataset_df)
    return dataset_df,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
