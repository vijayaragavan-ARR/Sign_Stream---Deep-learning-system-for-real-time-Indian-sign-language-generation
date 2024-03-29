using UnrealBuildTool;

public class SignStreamClientTarget : TargetRules
{
	public SignStreamClientTarget(TargetInfo Target) : base(Target)
	{
		DefaultBuildSettings = BuildSettingsVersion.V3;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		Type = TargetType.Client;
		ExtraModuleNames.Add("SignStream");
	}
}
