using UnrealBuildTool;

public class SignStreamEditorTarget : TargetRules
{
	public SignStreamEditorTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Editor;
		ExtraModuleNames.Add("SignStream");
	}
}
