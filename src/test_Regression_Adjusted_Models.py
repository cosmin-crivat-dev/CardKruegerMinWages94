import pandas as pd
import statsmodels.formula.api as smf


class Test_Regression_Adjusted_Models:
    """Generate the two requested regression specifications."""

    CHARACTERISTICS = [
        "CHAIN", "CO_OWNED", "EMPFT", "EMPPT", "NMGRS", "WAGE_ST",
        "PCTAFF", "MEALS", "OPEN", "HRSOPEN", "PSODA", "PFRY", "PENTREE",
        "NREGS", "NREGS11",
    ]

    def generate_models(self, data_frame: pd.DataFrame) -> dict[str, object]:
        """Fit and return models (1a) and (1b) for the supplied data frame.

        The outcome is the change in FTE employment from wave 1 to wave 2.
        Model (1a) includes store characteristics and the New Jersey dummy;
        model (1b) replaces the NJ dummy with the treatment GAP variable.
        """
        required_columns = {
            "FTE1", "FTE2", "GAP", "STATE", *self.CHARACTERISTICS
        }
        missing_columns = required_columns.difference(data_frame.columns)
        if missing_columns:
            raise ValueError(
                "Data frame is missing required columns: "
                + ", ".join(sorted(missing_columns))
            )

        model_data = data_frame.copy()
        model_data["AE"] = model_data["FTE2"] - model_data["FTE1"]
        model_data["NJ"] = (model_data["STATE"] == "New Jersey").astype(int)

        # Categorical codes are treated as categories, not continuous numbers.
        characteristic_terms = [
            "C(CHAIN)",
            "C(CO_OWNED)",
            "EMPFT",
            "EMPPT",
            "NMGRS",
            "WAGE_ST",
            "PCTAFF",
            "C(MEALS)",
            "OPEN",
            "HRSOPEN",
            "PSODA",
            "PFRY",
            "PENTREE",
            "NREGS",
            "NREGS11",
        ]
        characteristics = " + ".join(characteristic_terms)
        model_a = smf.ols(f"AE ~ {characteristics} + NJ", data=model_data).fit()
        model_b = smf.ols(f"AE ~ {characteristics} + GAP", data=model_data).fit()

        return {"1a": model_a, "1b": model_b}

    def show_model_coefficients(
        self, models: dict[str, object]
    ) -> pd.DataFrame:
        """Print and return a compact Table 4-style coefficient table.

        Each cell contains the coefficient followed by its standard error in
        parentheses. The fitted model objects are those returned by
        :meth:`generate_models`.
        """
        model_labels = {"1a": "(i)", "1b": "(ii)"}
        terms = set()
        for model in models.values():
            terms.update(model.params.index)

        term_labels = {
            "Intercept": "Constant",
            "NJ": "New Jersey dummy",
            "GAP": "Initial wage gap",
        }
        ordered_terms = sorted(
            terms,
            key=lambda term: (
                {"Intercept": 0, "NJ": 1, "GAP": 2}.get(term, 3),
                term,
            ),
        )
        table = pd.DataFrame(
            index=[term_labels.get(term, term) for term in ordered_terms],
            columns=[model_labels.get(name, name) for name in models],
        )

        for name, model in models.items():
            label = model_labels.get(name, name)
            for term in ordered_terms:
                if term in model.params.index:
                    table.loc[term_labels.get(term, term), label] = (
                        f"{model.params[term]:.2f}\n"
                        f"({model.bse[term]:.2f})"
                    )

        table.loc["Standard error of regression"] = [
            f"{model.mse_resid ** 0.5:.2f}" for model in models.values()
        ]
        table.loc["R-squared"] = [
            f"{model.rsquared:.2f}" for model in models.values()
        ]
        print("TABLE 4 - REDUCED-FORM MODELS FOR CHANGE IN EMPLOYMENT")
        print(table.to_string())
        return table

